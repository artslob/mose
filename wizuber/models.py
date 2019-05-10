from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class WizuberUser(AbstractUser):
    first_name = models.CharField(_('first name'), max_length=30, blank=False)
    last_name = models.CharField(_('last name'), max_length=30, blank=False)
    middle_name = models.CharField(_('middle name'), max_length=30, null=True, blank=True)
    email = models.EmailField(_('email address'), blank=False, unique=True)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']


class Wizard(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        if self.middle_name:
            return f'{self.name} {self.surname} {self.middle_name}'
        return f'{self.name} {self.surname}'


class Customer(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, null=True, blank=True)


class Wishes(models.Model):
    creator = models.ForeignKey(Customer, on_delete=models.CASCADE)
    description = models.TextField()
    owner = models.ForeignKey(Wizard, on_delete=models.CASCADE, null=True, blank=True)
