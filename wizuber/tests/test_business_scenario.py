from typing import Iterable

from django.test import TestCase
from django.urls import reverse

from wizuber.models import Wish, Customer, WishStatus, Wizard, CandleMaterial, SizeChoices

# constants
CUSTOMER_BALANCE = 500
WISH_PRICE = 42
WISH_DESC = 'test wish'


class PrimaryBusinessScenario(TestCase):
    def setUp(self) -> None:
        self.customer = Customer.objects.create_user('test_customer', 'customer@test.com', '123')
        self.wizard = Wizard.objects.create_user('test_wizard', 'wizard@test.com', '123')

    def check_available_actions(self, wish, expected_action_names: Iterable[str]):
        url = reverse('wizuber:detail-wish', kwargs=dict(pk=wish.pk))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        actions = set(action.get_action_name() for action in response.context['actions'])
        self.assertEqual(actions, set(expected_action_names))

    def refresh(self, wish=None):
        self.customer.refresh_from_db()
        self.wizard.refresh_from_db()
        if wish is not None:
            wish.refresh_from_db()

    def test_db_state(self):
        self.assertEqual(Wish.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(Wizard.objects.count(), 1)

    def test_business_scenario(self):
        # test wish creating
        self.assertEqual(Wish.objects.count(), 0)
        self.client.force_login(self.customer)
        url = reverse('wizuber:create-wish')
        response = self.client.post(url, dict(description=WISH_DESC, price=WISH_PRICE))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Wish.objects.count(), 1)

        # check wish created
        wish = Wish.objects.first()
        self.assertEqual(wish.creator, self.customer)
        self.assertEqual(wish.price, WISH_PRICE)
        self.assertEqual(wish.description, WISH_DESC)
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

        # check wizard own wish
        self.client.force_login(self.wizard)
        self.check_available_actions(wish, ['own'])

        url = reverse('wizuber:handle-wish-action', kwargs=dict(pk=wish.pk, action='own'))
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.refresh(wish)
        self.assertTrue(wish.in_status(WishStatus.WORK))
        self.assertTrue(wish.owner == wish.assigned_to == self.wizard)
        self.assertEqual(self.wizard.owned_wishes.count(), 1)
        self.assertEqual(wish.pentacle_artifacts.count(), 0)
        self.assertEqual(wish.candle_artifacts.count(), 0)
        self.assertFalse(wish.has_spirit_artifact())
        self.check_available_actions(wish, ['spirit-artifact', 'candle-artifact', 'pentacle-artifact'])

        # check pentacle artifact creation by wizard
        url = reverse('wizuber:handle-wish-action', kwargs=dict(pk=wish.pk, action='candle-artifact'))
        response = self.client.post(url, dict(material=CandleMaterial.TALLOW.name, size=SizeChoices.SMALL.name))
        self.assertEqual(response.status_code, 302)
        self.refresh(wish)
        self.assertEqual(wish.candle_artifacts.count(), 1)
        candle = wish.candle_artifacts.first()
        self.assertEqual(candle.wish, wish)
        self.assertEqual(candle.material, CandleMaterial.TALLOW.name)
        self.assertEqual(candle.size, SizeChoices.SMALL.name)
