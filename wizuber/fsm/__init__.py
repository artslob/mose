from typing import List, Type

from wizuber.fsm.action import IAction
from wizuber.fsm.exception import ActionAccessDenied, ActionNotFound


def action_names() -> List[str]:
    return list(IAction.defined_actions.keys())


def action_classes() -> List[Type[IAction]]:
    return list(IAction.defined_actions.values())


def action_class_by_name(name: str) -> Type[IAction]:
    try:
        return IAction.defined_actions[name]
    except KeyError:
        msg = f"action with name {name!r} not found"
        raise ActionNotFound(msg) from None


__all__ = [
    action_names,
    action_classes,
    action_class_by_name,
    IAction,
    ActionNotFound,
    ActionAccessDenied,
]
