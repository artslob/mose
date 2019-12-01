from typing import Iterable

from django.test import TestCase
from django.urls import reverse

from wizuber.models import Wish, Customer, WishStatus

# constants
CUSTOMER_BALANCE = 500


class PrimaryBusinessScenario(TestCase):
    def setUp(self) -> None:
        self.wish_price = 42
        self.wish_desc = 'test wish'
        self.customer = Customer.objects.create_user('test_customer', 'customer@test.com', '123')

    def check_available_actions(self, wish, expected_action_names: Iterable[str]):
        url = reverse('wizuber:detail-wish', kwargs=dict(pk=wish.pk))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        actions = set(action.get_action_name() for action in response.context['actions'])
        self.assertEqual(actions, set(expected_action_names))

    def refresh(self, wish=None):
        self.customer.refresh_from_db()
        if wish is not None:
            wish.refresh_from_db()

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
        self.assertEqual(wish.status, WishStatus.NEW.name)
        self.assertTrue(wish.in_status(WishStatus.NEW))

        self.check_available_actions(wish, ['pay', 'delete'])

        # pay for wish
        self.refresh(wish)
        self.assertEqual(self.customer.balance, CUSTOMER_BALANCE)
        url = reverse('wizuber:handle-wish-action', kwargs=dict(pk=wish.pk, action='pay'))
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.refresh(wish)
        self.assertTrue(wish.in_status(WishStatus.ACTIVE))
        self.assertEqual(self.customer.balance, CUSTOMER_BALANCE - wish.price)
        self.check_available_actions(wish, [])
