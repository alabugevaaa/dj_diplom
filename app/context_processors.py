from app.models import Category


def get_menu(request):
    menu = Category.objects.filter(parent__isnull=True).prefetch_related('categories')
    context = {'menu': menu}

    return context
