from typing import Iterable

from django.test import TestCase
from django.urls import reverse

from wizuber.models import Wish, Customer, WishStatus, Wizard, CandleMaterial, SizeChoices, Student, Spirit, \
    SpiritGrades, WizuberUser, BaseArtifact

# constants
CUSTOMER_BALANCE = 500
WIZARD_START_BALANCE = 13
WISH_PRICE = 42
WISH_DESC = 'test wish'


class PrimaryBusinessScenario(TestCase):
    def setUp(self) -> None:
        self.customer = Customer.objects.create_user('test_customer', 'customer@test.com', '123')
        self.wizard = Wizard.objects.create_user('test_wizard', 'wizard@test.com', '123', balance=WIZARD_START_BALANCE)
        self.student = Student.objects.create_user('test_student', 'student@test.com', '123', teacher=self.wizard)
        self.spirit = Spirit.objects.create_user('test_spirit', 'spirit@test.com', '123',
                                                 grade=SpiritGrades.FOLIOT.name)

    # helper methods

    def check_available_actions(self, wish, expected_action_names: Iterable[str]):
        url = reverse('wizuber:detail-wish', kwargs=dict(pk=wish.pk))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        actions = set(action.get_action_name() for action in response.context['actions'])
        self.assertEqual(actions, set(expected_action_names))

    def refresh(self):
        self.customer.refresh_from_db()
        self.wizard.refresh_from_db()
        self.student.refresh_from_db()
        self.spirit.refresh_from_db()
        if self.wish is not None:
            self.wish.refresh_from_db()

    def get_url_for_action(self, action_name: str):
        kwargs = dict(pk=self.wish.pk, action=action_name)
        return reverse('wizuber:handle-wish-action', kwargs=kwargs)

    # tests

    def test_db_state(self):
        self.assertEqual(Wish.objects.count(), 0)
        self.assertEqual(WizuberUser.objects.count(), 4)
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(Wizard.objects.count(), 1)
        self.assertEqual(Student.objects.count(), 1)
        self.assertEqual(Spirit.objects.count(), 1)

    def test_wish_deletion(self):
        self.wish_creating()
        self.check_created_wish_attributes()

        response = self.client.post(self.get_url_for_action('delete'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Wish.objects.count(), 0)

    def test_artifact_deletion(self):
        self.wish_creating()
        self.check_created_wish_attributes()
        self.pay_for_wish()
        self.wizard_own_wish()

        # check candle artifact is deleted
        self.candle_artifact_creation()
        self.check_available_actions(self.wish, [
            'spirit-artifact', 'candle-artifact', 'pentacle-artifact', 'to-student'
        ])
        self.assertEqual(BaseArtifact.objects.count(), 1)
        url = reverse('wizuber:delete-artifact', kwargs=dict(pk=self.wish.candle_artifacts.first().pk))
        response = self.client.post(url)
        self.assertRedirects(response, self.wish.get_absolute_url())
        self.assertEqual(BaseArtifact.objects.count(), 0)
        self.check_available_actions(self.wish, [
            'spirit-artifact', 'candle-artifact', 'pentacle-artifact', 'to-student'
        ])

        # check pentacle artifact is deleted
        self.check_pentacle_artifact_creation()
        self.assertEqual(BaseArtifact.objects.count(), 1)
        url = reverse('wizuber:delete-artifact', kwargs=dict(pk=self.wish.pentacle_artifacts.first().pk))
        response = self.client.post(url)
        self.assertRedirects(response, self.wish.get_absolute_url())
        self.assertEqual(BaseArtifact.objects.count(), 0)
        self.check_available_actions(self.wish, [
            'spirit-artifact', 'candle-artifact', 'pentacle-artifact', 'to-student'
        ])

        # check spirit artifact is deleted
        self.check_spirit_artifact_creation()
        self.assertEqual(BaseArtifact.objects.count(), 1)
        url = reverse('wizuber:delete-artifact', kwargs=dict(pk=self.wish.spirit_artifact.pk))
        response = self.client.post(url)
        self.assertRedirects(response, self.wish.get_absolute_url())
        self.assertEqual(BaseArtifact.objects.count(), 0)
        self.check_available_actions(self.wish, [
            'spirit-artifact', 'candle-artifact', 'pentacle-artifact', 'to-student'
        ])

    def test_business_scenario(self):
        self.wish_creating()
        wish = self.check_created_wish_attributes()
        self.pay_for_wish()
        self.wizard_own_wish()
        self.candle_artifact_creation()

        # check assign to student
        response = self.client.post(self.get_url_for_action('to-student'))
        self.assertEqual(response.status_code, 302)
        self.refresh()
        self.assertTrue(wish.owner == self.wizard)
        self.assertTrue(wish.assigned_to == self.student)

        # check pentacle artifact creation by student
        self.client.force_login(self.student)
        self.check_available_actions(wish, ['to-wizard', 'spirit-artifact', 'candle-artifact', 'pentacle-artifact'])
        self.check_pentacle_artifact_creation()
        self.check_available_actions(wish, ['to-wizard', 'spirit-artifact', 'candle-artifact', 'pentacle-artifact'])

        # check spirit artifact creation by student
        response = self.client.post(self.get_url_for_action('spirit-artifact'), dict(spirit=self.spirit.pk))
        self.assertEqual(response.status_code, 302)
        self.refresh()
        self.assertTrue(wish.has_spirit_artifact())
        self.assertEqual(wish.spirit_artifact.wish, wish)
        self.assertEqual(wish.spirit_artifact.spirit, self.spirit)
        self.check_available_actions(wish, ['to-wizard', 'spirit-artifact', 'candle-artifact', 'pentacle-artifact'])

        # check assign to wizard
        response = self.client.post(self.get_url_for_action('to-wizard'))
        self.assertEqual(response.status_code, 302)
        self.refresh()
        self.assertTrue(wish.owner == self.wizard)
        self.assertTrue(wish.assigned_to == self.wizard)

        # check assign to spirit
        self.client.force_login(self.wizard)
        self.check_available_actions(wish, [
            'candle-artifact', 'spirit-artifact', 'pentacle-artifact', 'to-student', 'to-spirit'
        ])

        response = self.client.post(self.get_url_for_action('to-spirit'))
        self.assertEqual(response.status_code, 302)
        self.refresh()
        self.assertTrue(wish.in_status(WishStatus.ON_SPIRIT))
        self.assertEqual(wish.owner, self.wizard)
        self.assertEqual(wish.assigned_to, self.spirit)

        # check assign from spirit to wizard
        self.client.force_login(self.spirit)
        self.check_available_actions(wish, ['spirit-to-wizard'])

        response = self.client.post(self.get_url_for_action('spirit-to-wizard'))
        self.assertEqual(response.status_code, 302)
        self.refresh()
        self.assertTrue(wish.in_status(WishStatus.READY))
        self.assertTrue(wish.owner == wish.assigned_to == self.wizard)

        # check close wish
        self.client.force_login(self.wizard)
        self.check_available_actions(wish, ['close'])
        self.assertEqual(self.wizard.balance, WIZARD_START_BALANCE)

        response = self.client.post(self.get_url_for_action('close'))
        self.assertEqual(response.status_code, 302)
        self.refresh()
        self.assertTrue(wish.in_status(WishStatus.CLOSED))
        self.assertTrue(wish.owner == self.wizard)
        self.assertTrue(wish.creator == wish.assigned_to == self.customer)
        self.assertEqual(self.wizard.balance, WIZARD_START_BALANCE + wish.price)

    # tests component parts

    def wish_creating(self):
        self.assertEqual(Wish.objects.count(), 0)
        self.client.force_login(self.customer)
        url = reverse('wizuber:create-wish')
        response = self.client.post(url, dict(description=WISH_DESC, price=WISH_PRICE))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Wish.objects.count(), 1)

    def check_created_wish_attributes(self):
        self.wish = wish = Wish.objects.first()
        self.assertEqual(wish.creator, self.customer)
        self.assertEqual(wish.price, WISH_PRICE)
        self.assertEqual(wish.description, WISH_DESC)
        self.assertTrue(wish.owner is wish.assigned_to is None)
        self.assertEqual(wish.status, WishStatus.NEW.name)
        self.assertTrue(wish.in_status(WishStatus.NEW))

        self.check_available_actions(wish, ['pay', 'delete'])

        return wish

    def pay_for_wish(self):
        self.refresh()
        self.assertEqual(self.customer.balance, CUSTOMER_BALANCE)
        response = self.client.post(self.get_url_for_action('pay'))
        self.assertEqual(response.status_code, 302)
        self.refresh()
        self.assertTrue(self.wish.in_status(WishStatus.ACTIVE))
        self.assertEqual(self.customer.balance, CUSTOMER_BALANCE - self.wish.price)
        self.check_available_actions(self.wish, [])

    def wizard_own_wish(self):
        self.client.force_login(self.wizard)
        self.check_available_actions(self.wish, ['own'])

        response = self.client.post(self.get_url_for_action('own'))
        self.assertEqual(response.status_code, 302)
        self.refresh()
        self.assertTrue(self.wish.in_status(WishStatus.WORK))
        self.assertTrue(self.wish.owner == self.wish.assigned_to == self.wizard)
        self.assertEqual(self.wizard.owned_wishes.count(), 1)
        self.assertEqual(self.wish.pentacle_artifacts.count(), 0)
        self.assertEqual(self.wish.candle_artifacts.count(), 0)
        self.assertFalse(self.wish.has_spirit_artifact())
        self.check_available_actions(self.wish, [
            'spirit-artifact', 'candle-artifact', 'pentacle-artifact', 'to-student'
        ])

    def candle_artifact_creation(self):
        response = self.client.post(self.get_url_for_action('candle-artifact'),
                                    dict(material=CandleMaterial.TALLOW.name, size=SizeChoices.SMALL.name))
        self.assertEqual(response.status_code, 302)
        self.refresh()
        self.assertEqual(self.wish.candle_artifacts.count(), 1)
        candle = self.wish.candle_artifacts.first()
        self.assertEqual(candle.wish, self.wish)
        self.assertEqual(candle.material, CandleMaterial.TALLOW.name)
        self.assertEqual(candle.size, SizeChoices.SMALL.name)

    def check_pentacle_artifact_creation(self):
        response = self.client.post(self.get_url_for_action('pentacle-artifact'),
                                    dict(name='some test pentacle', size=SizeChoices.LARGE.name))
        self.assertEqual(response.status_code, 302)
        self.refresh()
        self.assertEqual(self.wish.pentacle_artifacts.count(), 1)
        pentacle = self.wish.pentacle_artifacts.first()
        self.assertEqual(pentacle.wish, self.wish)
        self.assertEqual(pentacle.name, 'some test pentacle')
        self.assertEqual(pentacle.size, SizeChoices.LARGE.name)

    def check_spirit_artifact_creation(self):
        response = self.client.post(self.get_url_for_action('spirit-artifact'), dict(spirit=self.spirit.pk))
        self.assertEqual(response.status_code, 302)
        self.refresh()
        self.assertTrue(self.wish.has_spirit_artifact())
        self.assertEqual(self.wish.spirit_artifact.wish, self.wish)
        self.assertEqual(self.wish.spirit_artifact.spirit, self.spirit)
