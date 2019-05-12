from enum import Enum

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class WizuberUser(AbstractUser):
    first_name = models.CharField(_('first name'), max_length=30, blank=False)
    last_name = models.CharField(_('last name'), max_length=30, blank=False)
    middle_name = models.CharField(_('middle name'), max_length=30, null=True, blank=True)
    email = models.EmailField(_('email address'), blank=False, unique=True)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def is_customer(self):
        return hasattr(self, 'customer')

    def is_wizard(self):
        return hasattr(self, 'wizard')


class Wizard(models.Model):
    profile = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE)

    def __str__(self):
        self.profile: WizuberUser
        return self.profile.username


class Customer(models.Model):
    profile = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE)

    def __str__(self):
        self.profile: WizuberUser
        return self.profile.username


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


class RightsSupport(models.Model):
    class Meta:
        # No database table creation or deletion operations will be performed for this model.
        managed = False
        permissions = (
            ('customer', 'Global customer rights'),
            ('wizard', 'Global wizard rights'),
        )
