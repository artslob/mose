from abc import ABCMeta, abstractmethod
from typing import Type

from wizuber.fsm.form import IForm, DeleteForm
from wizuber.models import Wish, WizuberUser


class IAction(metaclass=ABCMeta):
    def __init__(self, wish: Wish, user: WizuberUser, *args, **kwargs):
        self.wish = wish
        self.user = user

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
    def form_class(cls) -> Type[IForm]:
        return DeleteForm

    def is_available(self) -> bool:
        """ Delete action is always available for user-creator. """
        return self.wish.creator == self.user
