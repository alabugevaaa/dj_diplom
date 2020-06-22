import copy

from django.contrib.auth import logout, authenticate, login
from django.core.cache import cache
from django.http import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import FormView

from .forms import ReviewForm, LoginForm, RegisterForm
from .models import Item, Article, Category, Review, Order, OrderDetail


def logout_view(request):
    cache.delete(request.user.username)
    logout(request)
    return redirect(login_view)


def login_view(request):
    context = {}
    next = request.POST.get('next', request.GET.get('next', ''))
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if next:
                return redirect(next)
            return redirect(main)
        else:
            context['error'] = True
    context['form'] = form

    return render(request, 'store/login_form.html', context)


def registration(request):
    template_name = 'store/registration_form.html'
    context = {}
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            context['registered'] = True
        else:
            context['error'] = True
    else:
        form = RegisterForm()

    context['form'] = form
    return render(request, template_name, context)


def main(request):
    template_name = 'store/index.html'
    best_mobiles = Item.objects.filter(category__title='Смартфоны')[:3]
    articles = Article.objects.all().prefetch_related('items')[:3]

    context = {'items': best_mobiles,
               'articles': articles}
    return render(request, template_name, context)


def articles(request):
    template_name = 'store/articles.html'
    articles = Article.objects.all()

    context = {'articles': articles}
    return render(request, template_name, context)


def category_content(request, name):
    template_name = 'store/items.html'
    category = get_object_or_404(Category, alias=name)
    items = Item.objects.filter(category=category)
    context = {'items': items,
               'title': category.title}

    return render(request, template_name, context)


def show_item(request, slug):
    template_name = 'store/product.html'
    item = get_object_or_404(Item, slug=slug)
    reviews = Review.objects.filter(item=item)
    context = {
        'item': item,
        'reviews': reviews
    }
    return render(request, template_name, context)


class ItemView(FormView):

    template_name = 'store/product.html'
    form_class = ReviewForm

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        item = get_object_or_404(Item, slug=kwargs['slug'])
        reviews = Review.objects.filter(item=item)
        context['item'] = item
        context['reviews'] = reviews
        if request.user.is_authenticated:
            reviewed = reviews.filter(user=request.user).count()
            is_review_exist = True if reviewed > 0 else False
            context['is_review_exist'] = is_review_exist
        return self.render_to_response(context)

    def form_valid(self, form):
        feed = form.save(commit=False)
        feed.user = self.request.user
        item = get_object_or_404(Item, slug=self.kwargs['slug'])
        feed.item = item
        feed.save()
        return redirect(reverse('show_item', kwargs={'slug': self.kwargs['slug']}))


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 1}
        else:
            self.cart[product_id]['quantity'] += 1
        self.save()

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Item.objects.filter(id__in=product_ids)
        cart = copy.deepcopy(self.cart)
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['quantity'] = int(item['quantity'])
            yield item

    def __len__(self):
        return sum(int(item['quantity']) for item in self.cart.values())

    def clear(self):
        del self.session['cart']
        self.session.modified = True


def cart(request):
    user_cart = Cart(request)

    if request.method == "POST":
        item_id = request.POST.get('merchandise_id')
        item = get_object_or_404(Item, id=item_id)
        user_cart.add(item)

    total_count = len(user_cart)
    context = {
        'items': user_cart,
        'total_count': total_count
    }

    return render(request, 'store/cart.html', context)


def create_order(request):
    if not request.user.is_authenticated:
        return redirect('/login/?next=/cart/')
    else:
        if request.method == "POST":
            user = request.user
            cart = Cart(request)
            order = Order.objects.create(user=user)
            for item in cart:
                product = item['product']
                quantity = item['quantity']
                OrderDetail.objects.create(order=order, item=product, count=quantity)
            cart.clear()
            return render(request, 'store/order.html', {'order': order})
        else:
            return HttpResponseBadRequest()


