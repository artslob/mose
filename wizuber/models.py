from django.db import models


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
