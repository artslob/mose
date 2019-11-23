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

    is_wizard = False
    is_customer = False
    is_student = False
    is_spirit = False

    can_create_wish = False


class Wizard(WizuberUser):
    balance = models.PositiveIntegerField(default=0)

    is_wizard = True

    def has_student(self) -> bool:
        return hasattr(self, 'student')

    def get_absolute_url(self):
        return reverse('wizuber:detail-wizard', kwargs=dict(pk=self.id))

    def get_queryset_for_wish_list(self):
        return self.owned_wishes.all()


class Customer(WizuberUser):
    balance = models.PositiveIntegerField(default=500)

    is_customer = True
    can_create_wish = True

    def get_queryset_for_wish_list(self):
        return self.created_wishes.all()


class Student(WizuberUser):
    teacher = models.OneToOneField(Wizard, on_delete=models.CASCADE)

    is_student = True

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

    is_spirit = True

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
    # TODO check all on_delete parameters
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


class BaseArtifact(PolymorphicModel):
    pass


class SizeChoices(ChoicesEnum):
    LARGE = 'large'
    MEDIUM = 'medium'
    SMALL = 'small'

    @classmethod
    def default(cls):
        return cls.MEDIUM.name


class CandleMaterial(ChoicesEnum):
    TALLOW = 'tallow'
    BEESWAX = 'beeswax'
    PARAFFIN = 'paraffin'

    @classmethod
    def default(cls):
        return cls.TALLOW.name


class CandleArtifact(BaseArtifact):
    wish = models.ForeignKey(Wish, related_name='candle_artifacts', on_delete=models.CASCADE)
    SIZES = SizeChoices
    size = models.CharField(max_length=SIZES.max_length(), choices=SIZES.choices(), default=SIZES.default())
    MATERIALS = CandleMaterial
    material = models.CharField(
        max_length=MATERIALS.max_length(), choices=MATERIALS.choices(), default=MATERIALS.default()
    )


class PentacleArtifact(BaseArtifact):
    wish = models.ForeignKey(Wish, related_name='pentacle_artifacts', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    SIZES = SizeChoices
    size = models.CharField(max_length=SIZES.max_length(), choices=SIZES.choices(), default=SIZES.default())


class SpiritArtifact(BaseArtifact):
    wish = models.OneToOneField(Wish, related_name='spirit_artifact', on_delete=models.CASCADE)
    spirit = models.OneToOneField(Spirit, related_name='spirit_artifact', on_delete=models.CASCADE)


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
