from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from wizuber.models import Customer, Wizard, Wishes


class Command(BaseCommand):
    help = 'Populates database with initial data'

    def handle(self, *args, **options):
        admin, _ = get_user_model().objects.get_or_create(username='admin', email='admin@wizuber.com')
        admin.set_password('123')
        admin.is_superuser = True
        admin.is_staff = True
        admin.save()

        c1 = self._create_customer('c1')
        c2 = self._create_customer('c2')

        w1 = self._create_wizard('w1')
        w2 = self._create_wizard('w2')

        self._create_wish(c1, 'wish of user c1 without owner')
        self._create_wish(c2, 'wish of user c2 without owner')
        self._create_wish(c1, 'wish of user c1 with owner: wizard w1', w1)
        self._create_wish(c2, 'wish of user c2 with owner: wizard w2', w2)

        self.stdout.write(self.style.SUCCESS('Database successfully populated.'))

    @staticmethod
    def _create_wish(creator, description, owner=None):
        wish, _ = Wishes.objects.get_or_create(creator=creator.customer, description=description,
                                               owner=owner.wizard if owner else None)
        return wish

    @staticmethod
    def _create_user(username):
        user, _ = get_user_model().objects.get_or_create(
            username=username, first_name=f'{username} name', last_name=f'{username} last name',
            email=f'{username}@mail.com')
        user.set_password('123')
        user.save()
        return user

    @classmethod
    def _create_wizard(cls, username):
        wizard = cls._create_user(username)
        if not wizard.is_wizard():
            Wizard.objects.create(profile=wizard)
            wizard.groups.add(Group.objects.get(name='wizard'))
        return wizard

    @classmethod
    def _create_customer(cls, username):
        customer = cls._create_user(username)
        if not customer.is_customer():
            Customer.objects.create(profile=customer)
            customer.groups.add(Group.objects.get(name='customer'))
        return customer
