from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from wizuber.models import Customer, Wizard, Wish, Student, Spirit, SpiritGrades


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

        stud = self._create_student('stud', teacher=w1)

        bartimaeus = self._create_spirit('bartimaeus', SpiritGrades.DJINNI.name)
        self._create_spirit('spirit_under_w1', SpiritGrades.MARID.name, master=w1)
        self._create_spirit('spirit_under_w2', SpiritGrades.FOLIOT.name, master=w2)

        for _, grade in SpiritGrades.choices():
            for i in range(10):
                self._create_spirit(f'spirit_{grade}_{i}', grade)

        self._create_wish(c1, 'wish of user c1 without owner')
        self._create_wish(c2, 'wish of user c2 without owner')
        self._create_wish(c1, 'wish of user c1 with owner: wizard w1', w1)
        self._create_wish(c2, 'wish of user c2 with owner: wizard w2', w2)
        self._create_wish(c2, 'wish c2 with w2 and assigned to bartimaeus', w2, assigned_to=bartimaeus)
        self._create_wish(c2, 'wish c2 with w2 and assigned to student', w2, assigned_to=stud)

        for i in range(10):
            self._create_wish(c1, f'{i} wish', w1)

        self.stdout.write(self.style.SUCCESS('Database successfully populated.'))

    @staticmethod
    def _create_wish(creator, description, owner=None, **kwargs):
        status = Wish.STATUSES.WORK.name if owner else Wish.STATUSES.NEW.name
        get_or_create = Wish.objects.get_or_create
        wish, _ = get_or_create(creator=creator, description=description, owner=owner, status=status, **kwargs)
        return wish

    @staticmethod
    def _create_user(username, model, **kwargs):
        user, _ = model.objects.get_or_create(
            username=username, first_name=f'{username} name', last_name=f'{username} last name',
            email=f'{username}@mail.com', **kwargs
        )
        user.set_password('123')
        user.save()
        return user

    @classmethod
    def _create_wizard(cls, username):
        return cls._create_user(username, Wizard)

    @classmethod
    def _create_customer(cls, username):
        return cls._create_user(username, Customer)

    @classmethod
    def _create_student(cls, username, teacher):
        return cls._create_user(username, Student, teacher=teacher)

    @classmethod
    def _create_spirit(cls, username, grade: str, master: Wizard = None):
        return cls._create_user(username, Spirit, grade=grade, master=master)
