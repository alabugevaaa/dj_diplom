from django.test import TestCase

from app.models import Category, Item, Order


class AppTest(TestCase):
    fixtures = ['fixtures.json']

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_category(self):
        category = Category.objects.get(pk=6)
        response = self.client.get(f'/category/{category.alias}/')
        self.assertEqual(response.status_code, 200)

    def test_item(self):
        item = Item.objects.get(pk=6)
        response = self.client.get(f'/item/{item.slug}/')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.login(username='admin', password='admin')
        self.assertTrue(response)

    def test_add_to_cart(self):
        response = self.client.post('/cart/', {'merchandise_id': 6})
        total_count = response.context['total_count']
        self.assertEqual(total_count, 1)

    def test_create_order(self):
        self.client.login(username='admin', password='admin')
        self.client.post('/cart/', {'merchandise_id': 6})
        self.client.post('/order/', {})
        count = Order.objects.all().count()
        self.assertEqual(count, 1)
