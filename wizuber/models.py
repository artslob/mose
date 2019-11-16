from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
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
    balance = models.PositiveIntegerField(default=0)

    def get_absolute_url(self):
        return reverse('wizuber:detail-wizard', kwargs=dict(pk=self.id))

    def get_queryset_for_wish_list(self):
        return self.owned_wishes.all()


class Customer(WizuberUser):
    balance = models.PositiveIntegerField(default=500)

    def get_queryset_for_wish_list(self):
        return self.created_wishes.all()

    can_create_wish = True


class Student(WizuberUser):
    teacher = models.OneToOneField(Wizard, on_delete=models.CASCADE)

    def get_queryset_for_wish_list(self):
        return self.assigned_wishes.all()


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
    master = models.ForeignKey(Wizard, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    GRADES = SpiritGrades
    grade = models.CharField(max_length=GRADES.max_length(), choices=GRADES.choices())

    def get_queryset_for_wish_list(self):
        return self.assigned_wishes.all()


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
    creator = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='created_wishes')
    description = models.TextField()
    owner = models.ForeignKey(Wizard, on_delete=models.CASCADE, null=True, blank=True, related_name='owned_wishes')
    STATUSES = WishStatus
    status = models.CharField(max_length=STATUSES.max_length(), choices=STATUSES.choices(), default=STATUSES.default())
    assigned_to = models.ForeignKey(WizuberUser, related_name='assigned_wishes', on_delete=models.SET_NULL,
                                    null=True, blank=True)
    price = models.PositiveIntegerField(validators=[MinValueValidator(limit_value=1)], default=50)

    def get_absolute_url(self):
        return reverse('wizuber:detail-wish', kwargs=dict(pk=self.id))

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
