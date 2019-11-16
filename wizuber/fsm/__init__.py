from enum import Enum, unique
from typing import Type, List

from wizuber.fsm.action import IAction, DeleteAction


@unique
class ActionMapping(Enum):
    DELETE = DeleteAction

    @staticmethod
    def action_classes() -> List[Type[IAction]]:
        return [cls for cls in IAction.defined_actions.values()]

    @staticmethod
    def action_class_by_name(name: str) -> Type[IAction]:
        return IAction.defined_actions[name]


__all__ = [ActionMapping, IAction, DeleteAction]
