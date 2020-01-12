from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from wizuber.models import (
    Customer,
    Wizard,
    Wish,
    Student,
    Spirit,
    SpiritGrades,
    CandleArtifact,
    SizeChoices,
    CandleMaterial,
    PentacleArtifact,
    SpiritArtifact,
)


class Command(BaseCommand):
    help = "Populates database with initial data"

    def handle(self, *args, **options):
        admin, _ = get_user_model().objects.get_or_create(
            username="admin", email="admin@wizuber.com"
        )
        admin.set_password("123")
        admin.is_superuser = True
        admin.is_staff = True
        admin.save()

        c1 = self._create_customer("c1")
        c2 = self._create_customer("c2")

        w1 = self._create_wizard("w1")
        w2 = self._create_wizard("w2")

        student = self._create_student("student", teacher=w1)

        bartimaeus = self._create_spirit("bartimaeus", SpiritGrades.DJINNI.name)
        spirit = self._create_spirit("spirit", SpiritGrades.DJINNI.name)
        self._create_spirit("spirit_under_w1", SpiritGrades.MARID.name, master=w1)
        self._create_spirit("spirit_under_w2", SpiritGrades.FOLIOT.name, master=w2)

        for _, grade in SpiritGrades.choices():
            for i in range(10):
                self._create_spirit(f"spirit_{grade.lower()}_{i}", grade)

        self._create_wish(c1, "new wish")
        self._create_wish(c1, "payed wish", status=Wish.STATUSES.ACTIVE.name)

        owned_wish = self._create_wish(c1, "owned wish", owner=w1)
        self._create_artifact(
            CandleArtifact,
            owned_wish,
            size=SizeChoices.LARGE.name,
            material=CandleMaterial.PARAFFIN.name,
        )
        self._create_artifact(
            CandleArtifact,
            owned_wish,
            size=SizeChoices.SMALL.name,
            material=CandleMaterial.TALLOW.name,
        )
        self._create_artifact(
            PentacleArtifact,
            owned_wish,
            name="great big pentacle",
            size=SizeChoices.LARGE.name,
        )
        self._create_artifact(
            PentacleArtifact,
            owned_wish,
            name="additional small",
            size=SizeChoices.SMALL.name,
        )
        self._create_artifact(SpiritArtifact, owned_wish, spirit=spirit)

        self._create_wish(c1, "wish of user c1 without owner")
        self._create_wish(c2, "wish of user c2 without owner")
        self._create_wish(c1, "wish of user c1 with owner: wizard w1", w1)
        self._create_wish(c2, "wish of user c2 with owner: wizard w2", w2)
        self._create_wish(
            c1, "wish c1 with w1 and assigned to student", w1, assigned_to=student
        )
        for spirit_object in bartimaeus, spirit:
            for wizard in w1, w2:
                self._create_wish(
                    c1,
                    f"wish c1 with {wizard} and assigned to {spirit_object}",
                    wizard,
                    assigned_to=spirit_object,
                    status=Wish.STATUSES.ON_SPIRIT.name,
                )

        self._create_wish(c1, "ready wish 1", owner=w1, status=Wish.STATUSES.READY.name)
        self._create_wish(c1, "ready wish 2", owner=w1, status=Wish.STATUSES.READY.name)

        self._create_wish(
            c1,
            "closed wish 1",
            owner=w1,
            status=Wish.STATUSES.CLOSED.name,
            assigned_to=c1,
        )
        self._create_wish(
            c1,
            "closed wish 2",
            owner=w1,
            status=Wish.STATUSES.CLOSED.name,
            assigned_to=c1,
        )

        for i in range(10):
            self._create_wish(c1, f"{i} wish", w1)

        self.stdout.write(self.style.SUCCESS("Database successfully populated."))

    @staticmethod
    def _create_wish(creator, description, owner=None, assigned_to=None, status=None):
        if status is None:
            status = Wish.STATUSES.WORK.name if owner else Wish.STATUSES.NEW.name
        assigned_to = assigned_to if assigned_to else owner

        wish, _ = Wish.objects.get_or_create(
            creator=creator,
            description=description,
            assigned_to=assigned_to,
            owner=owner,
            status=status,
        )
        return wish

    @staticmethod
    def _create_artifact(model, wish, **kwargs):
        artifact, _ = model.objects.get_or_create(wish=wish, **kwargs)
        return artifact

    @staticmethod
    def _create_user(username, model, **kwargs):
        user, _ = model.objects.get_or_create(
            username=username,
            first_name=f"{username} name",
            last_name=f"{username} last name",
            email=f"{username}@mail.com",
            **kwargs,
        )
        user.set_password("123")
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
