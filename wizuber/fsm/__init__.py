from enum import Enum, unique
from typing import Type, List

from wizuber.fsm.action import IAction, DeleteAction, PayAction, OwnAction


@unique
class ActionMapping(Enum):
    DELETE = DeleteAction
    PAY = PayAction
    OWN = OwnAction

    @staticmethod
    def action_classes() -> List[Type[IAction]]:
        return list(IAction.defined_actions.values())

    @staticmethod
    def action_class_by_name(name: str) -> Type[IAction]:
        return IAction.defined_actions[name]


__all__ = [ActionMapping, IAction, DeleteAction, PayAction, OwnAction]
