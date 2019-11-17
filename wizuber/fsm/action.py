import inspect
from abc import ABCMeta, abstractmethod
from typing import Type

from wizuber.fsm.form import IForm, DeleteForm, PayForm
from wizuber.models import Wish, WizuberUser


class IAction(metaclass=ABCMeta):
    defined_actions = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        action_name = cls.get_action_name()
        if action_name in cls.defined_actions and not inspect.isabstract(cls):
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

    @classmethod
    def get_template_name(cls) -> str:
        return cls.form_class().get_full_template_name()

    def do_action(self, *args, **kwargs):
        pass


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


class PayAction(IAction):
    @classmethod
    def get_action_name(cls) -> str:
        return 'pay'

    @classmethod
    def get_action_description(cls) -> str:
        return 'To make wish visible for wizard pay for this wish'

    @classmethod
    def form_class(cls) -> Type[IForm]:
        return PayForm

    def is_available(self) -> bool:
        return self.wish.creator == self.user and self.wish.status == self.wish.STATUSES.NEW.name
