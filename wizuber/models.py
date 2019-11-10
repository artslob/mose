from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from polymorphic.managers import PolymorphicManager
from polymorphic.models import PolymorphicModel

from wizuber.const import CUSTOMER_PERM, WIZARD_PERM, STUDENT_PERM, SPIRIT_PERM
from wizuber.helpers import ChoicesEnum


class PolymorphicUserManager(PolymorphicManager, UserManager):
    pass


class WizuberUser(PolymorphicModel, AbstractUser):
    first_name = models.CharField(_('first name'), max_length=30, blank=False)
    last_name = models.CharField(_('last name'), max_length=30, blank=False)
    middle_name = models.CharField(_('middle name'), max_length=30, null=True, blank=True)
    email = models.EmailField(_('email address'), blank=False, unique=True)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    objects = PolymorphicUserManager()

    def get_queryset_for_wish_list(self):
        return Wish.objects.none()

    can_create_wish = False


class Wizard(WizuberUser):
    def get_queryset_for_wish_list(self):
        return Wish.objects.filter(owner=self)


class Customer(WizuberUser):
    def get_queryset_for_wish_list(self):
        return Wish.objects.filter(creator=self)

    can_create_wish = True


class Student(WizuberUser):
    teacher = models.OneToOneField(Wizard, on_delete=models.CASCADE)

    def get_queryset_for_wish_list(self):
        return Wish.objects.none()  # TODO


class SpiritGrades(ChoicesEnum):
    IMP = 'Imp'
    FOLIOT = 'Foliot'
    DJINNI = 'Djinni'
    AFRIT = 'Afrit'
    MARID = 'Marid'

    @classmethod
    def default(cls):
        return super().default()


class Spirit(WizuberUser):
    # TODO change cascade to set null and fix default to null
    master = models.ForeignKey(Wizard, on_delete=models.CASCADE, null=True, default=True, blank=True)
    GRADES = SpiritGrades
    grade = models.CharField(max_length=GRADES.max_length(), choices=GRADES.choices())

    def get_queryset_for_wish_list(self):
        return Wish.objects.none()  # TODO


class WishStatus(ChoicesEnum):
    NEW = 'New'
    ACTIVE = 'Active'
    WORK = 'Work'
    READY = 'Ready'
    CLOSED = 'Closed'
    CANCELED = 'Canceled'

    @classmethod
    def default(cls):
        return cls.NEW.name


class Wish(models.Model):
    creator = models.ForeignKey(Customer, on_delete=models.CASCADE)
    description = models.TextField()
    owner = models.ForeignKey(Wizard, on_delete=models.CASCADE, null=True, blank=True)
    STATUSES = WishStatus
    status = models.CharField(max_length=STATUSES.max_length(), choices=STATUSES.choices(), default=STATUSES.default())

    def get_statuses(self):
        return self.STATUSES


class RightsSupport(models.Model):
    class Meta:
        # No database table creation or deletion operations will be performed for this model.
        managed = False
        permissions = (
            (CUSTOMER_PERM, 'Global customer rights'),
            (WIZARD_PERM, 'Global wizard rights'),
            (STUDENT_PERM, 'Global student rights'),
            (SPIRIT_PERM, 'Global spirit rights'),
        )


def is_wizard(user):
    return isinstance(user, Wizard)


def is_customer(user):
    return isinstance(user, Customer)


def is_student(user):
    return isinstance(user, Student)


def is_spirit(user):
    return isinstance(user, Spirit)
