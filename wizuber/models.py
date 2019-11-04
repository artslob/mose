from enum import Enum

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from polymorphic.managers import PolymorphicManager
from polymorphic.models import PolymorphicModel


class PolymorphicUserManager(PolymorphicManager, UserManager):
    pass


class WizuberUser(PolymorphicModel, AbstractUser):
    first_name = models.CharField(_('first name'), max_length=30, blank=False)
    last_name = models.CharField(_('last name'), max_length=30, blank=False)
    middle_name = models.CharField(_('middle name'), max_length=30, null=True, blank=True)
    email = models.EmailField(_('email address'), blank=False, unique=True)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    objects = PolymorphicUserManager()

    def get_queryset_for_wish_list(self, model):
        return model.objects.none()

    @staticmethod
    def can_create_wish() -> bool:
        return False


class Wizard(WizuberUser):
    def get_queryset_for_wish_list(self, model):
        return model.objects.filter(owner=self)


class Customer(WizuberUser):
    def get_queryset_for_wish_list(self, model):
        return model.objects.filter(creator=self)

    @staticmethod
    def can_create_wish() -> bool:
        return True


class WishStatus(Enum):
    NEW = 'New'
    ACTIVE = 'Active'
    WORK = 'Work'
    READY = 'Ready'
    CLOSED = 'Closed'
    CANCELED = 'Canceled'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

    @classmethod
    def max_length(cls):
        return max(len(i.name) for i in cls)

    @classmethod
    def default(cls):
        return cls.NEW.name


class Wishes(models.Model):
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
            ('customer', 'Global customer rights'),
            ('wizard', 'Global wizard rights'),
        )
