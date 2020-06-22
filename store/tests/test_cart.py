from django.test import TestCase

from app.views import Cart
from app.models import Item, Category


class CartTest(TestCase):
    fixtures = ['fixtures.json']

    def setUp(self):
        self.product = Item.objects.get(pk=7)
        self.cart = Cart(self.client)

    def test_add(self):
        self.cart.add(self.product)
        self.assertEqual(len(self.cart), 1)

    def test_iter(self):
        for item in self.cart:
            name = item.name
            self.assertEqual(name, 'iPhone 7')

    def test_clear(self):
        self.cart.clear()
        self.assertEqual(len(self.cart), 0)
