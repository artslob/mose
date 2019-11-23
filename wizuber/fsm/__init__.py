from typing import Type, List

from wizuber.fsm.action import IAction, DeleteAction, PayAction, OwnAction


def action_classes() -> List[Type[IAction]]:
    return list(IAction.defined_actions.values())


def action_class_by_name(name: str) -> Type[IAction]:
    return IAction.defined_actions[name]


__all__ = [action_classes, action_class_by_name, IAction, DeleteAction, PayAction, OwnAction]
