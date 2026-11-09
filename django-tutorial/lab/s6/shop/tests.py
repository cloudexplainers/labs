from django.test import TestCase

from .models import Order, Tea


class ShopTests(TestCase):
    def setUp(self):
        Tea.objects.create(name="Sencha", slug="sencha", price="12.50", stock=3)

    def test_list_shows_teas(self):
        response = self.client.get("/")
        self.assertContains(response, "Sencha")

    def test_missing_tea_is_404(self):
        response = self.client.get("/teas/nope/")
        self.assertEqual(response.status_code, 404)

    def test_order_is_saved(self):
        data = {"quantity": 2, "email": "sam@example.com"}
        self.client.post("/teas/sencha/order/", data)
        self.assertEqual(Order.objects.count(), 1)

    def test_cannot_order_more_than_stock(self):
        data = {"quantity": 5, "email": "sam@example.com"}
        self.client.post("/teas/sencha/order/", data)
        self.assertEqual(Order.objects.count(), 0)
