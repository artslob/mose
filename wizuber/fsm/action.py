import inspect
from abc import ABCMeta, abstractmethod, ABC
from typing import Type

from django.db.models import F
from django.urls import reverse

from wizuber.fsm.form import IForm, DeleteForm, PayForm, OwnForm
from wizuber.models import Wish, WizuberUser, is_wizard, is_student


class IAction(metaclass=ABCMeta):
    defined_actions = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if inspect.isabstract(cls):
            return
        action_name = cls.get_action_name()
        if action_name in cls.defined_actions:
            raise RuntimeError(f'action name {action_name!r} is not unique!')
        cls.defined_actions[action_name] = cls

    def __init__(self, wish: Wish, user: WizuberUser, *args, **kwargs):
        self.wish = wish
        self.user = user

    @classmethod
    @abstractmethod
    def get_action_name(cls) -> str:
        pass

    @classmethod
    def template_name(cls) -> str:
        return cls.get_action_name()

    @classmethod
    def get_full_template_name(cls) -> str:
        return f'wizuber/action/{cls.template_name()}.html'

    @classmethod
    @abstractmethod
    def get_action_description(cls) -> str:
        pass

    @abstractmethod
    def is_available(self) -> bool:
        pass

    @classmethod
    @abstractmethod
    def form_class(cls) -> Type[IForm]:
        pass

    def is_processing_available(self) -> bool:
        return self.is_available() and self._is_processing_available()

    def _is_processing_available(self) -> bool:
        return True

    @abstractmethod
    def do_action(self):
        pass

    def get_success_url(self):
        return self.wish.get_absolute_url()


class DeleteAction(IAction):
    @classmethod
    def get_action_name(cls) -> str:
        return 'delete'

    @classmethod
    def get_action_description(cls) -> str:
        return 'You can delete this wish'

    @classmethod
    def form_class(cls) -> Type[IForm]:
        return DeleteForm

    def is_available(self) -> bool:
        """ Delete action is always available for user-creator. """
        return self.wish.creator == self.user

    def do_action(self):
        self.wish.delete()

    def get_success_url(self):
        return reverse('wizuber:list-wish')


class PayAction(IAction):
    @classmethod
    def get_action_name(cls) -> str:
        return 'pay'

    @classmethod
    def get_action_description(cls) -> str:
        return 'Pay for this with to make it visible for wizard'

    @classmethod
    def form_class(cls) -> Type[IForm]:
        return PayForm

    def is_available(self) -> bool:
        return self.wish.creator == self.user and self.wish.status == self.wish.STATUSES.NEW.name

    def _is_processing_available(self) -> bool:
        return self.user.balance >= self.wish.price

    def do_action(self):
        self.user.balance = F('balance') - self.wish.price
        self.user.save()
        self.user.refresh_from_db()
        self.wish.status = self.wish.STATUSES.ACTIVE.name
        self.wish.save()


class OwnAction(IAction):
    @classmethod
    def get_action_name(cls) -> str:
        return 'own'

    @classmethod
    def get_action_description(cls) -> str:
        return 'You can accept order for this wish'

    def is_available(self) -> bool:
        without_owner = self.wish.owner is None
        is_active_status = self.wish.status == self.wish.STATUSES.ACTIVE.name
        return is_wizard(self.user) and without_owner and is_active_status

    @classmethod
    def form_class(cls) -> Type[IForm]:
        return OwnForm

    def do_action(self):
        self.wish.owner = self.user
        self.wish.status = self.wish.STATUSES.WORK.name
        self.wish.save()


class ArtifactAction(IAction, ABC):
    @classmethod
    def get_action_description(cls) -> str:
        return 'You can add one or more artifacts to wish'

    def is_available(self) -> bool:
        user, wish = self.user, self.wish
        is_work_status = wish.status == wish.STATUSES.WORK.name

        if is_work_status and is_wizard(user) and wish.owner == user:
            return True

        if is_work_status and is_student(user) and wish.owner == user.teacher:
            return True

        return False
