from django.test import TestCase
from django.urls import reverse

from wizuber.models import Wish, Customer, WishStatus


class PrimaryBusinessScenario(TestCase):
    def setUp(self) -> None:
        self.wish_price = 42
        self.wish_desc = 'test wish'
        self.customer = Customer.objects.create_user('test_customer', 'customer@test.com', '123')

    def test_db_state(self):
        self.assertEqual(Wish.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 1)

    def test_business_scenario(self):
        # test wish creating
        self.assertEqual(Wish.objects.count(), 0)
        self.client.force_login(self.customer)
        url = reverse('wizuber:create-wish')
        response = self.client.post(url, dict(description=self.wish_desc, price=self.wish_price))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Wish.objects.count(), 1)

        # check wish created
        wish = Wish.objects.first()
        self.assertEqual(wish.creator, self.customer)
        self.assertEqual(wish.price, self.wish_price)
        self.assertEqual(wish.description, self.wish_desc)
        self.assertTrue(wish.owner is wish.assigned_to is None)
        self.assertTrue(wish.in_status(WishStatus.NEW))
