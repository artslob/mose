import inspect
from abc import ABC, ABCMeta, abstractmethod
from typing import Type

from django.db.models import F
from django.forms import ModelForm
from django.http import HttpRequest
from django.urls import reverse

from wizuber.fsm.exception import ActionAccessDenied
from wizuber.fsm.form import (
    CandleArtifactForm,
    PentacleArtifactForm,
    SpiritArtifactForm,
)
from wizuber.models import Wish, WizuberUser


class IAction(metaclass=ABCMeta):
    """
    Abstract class for all wish actions.
    New action classes are registered in `defined_actions` dict.
    """

    defined_actions = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if inspect.isabstract(cls):
            return
        action_name = cls.get_action_name()
        cls.validate_subclass_action_name(action_name)
        cls.defined_actions[action_name] = cls

    @classmethod
    def validate_subclass_action_name(cls, action_name: str):
        if action_name in cls.defined_actions:
            raise RuntimeError(
                f"action name {action_name!r} is not unique!"
            )  # pragma: no cover
        if not isinstance(action_name, str):
            raise RuntimeError(
                f"action name {action_name!r} should be string, got: {type(action_name)}"
            )  # pragma: no cover
        if action_name != action_name.lower() or " " in action_name:
            raise RuntimeError(
                f"action name should be in lowercase and without spaces: {action_name!r}"
            )  # pragma: no cover

    def __init__(self, wish: Wish, user: WizuberUser):
        """
        :param wish: instance of with to make action upon.
        :param user: logged-in user that want to make some action with this wish.
        """
        self.wish = wish
        self.user = user

    @classmethod
    @abstractmethod
    def get_action_name(cls) -> str:
        """
        Unique string that defines name of the action. Should be lowercase without spaces.
        By default equals to name of html template.
        For example: action with name 'pay' has template 'wizuber/action/pay.html'.
        """

    @classmethod
    def template_name(cls) -> str:
        return cls.get_action_name()

    @classmethod
    def get_full_template_name(cls) -> str:
        return f"wizuber/action/{cls.template_name()}.html"

    @classmethod
    @abstractmethod
    def get_action_description(cls) -> str:
        """ Human-readable prompt string that displayed at html template. """

    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if user can potentially make this action.
        If true, user can see this action on html template.
        """

    def is_processing_available(self) -> bool:
        """
        Check that user can see action and also execute it.
        e.g.: customer-creator of the wish can always see button for 'pay' action,
        but if user has not enough money to pay for wish button will be disabled
        and this method returns False.
        """
        return self.is_available() and self._is_processing_available()

    def _is_processing_available(self) -> bool:
        return True

    def execute(self, request: HttpRequest):
        if not self.is_processing_available():
            raise ActionAccessDenied

        return self._execute(request)

    @abstractmethod
    def _execute(self, request: HttpRequest):
        """
        Actual code of action should be here.
        All checks for permissions should be in `is_processing_available`.
        """

    def get_success_url(self):
        return self.wish.get_absolute_url()


class DeleteAction(IAction):
    @classmethod
    def get_action_name(cls) -> str:
        return "delete"

    @classmethod
    def get_action_description(cls) -> str:
        return "You can delete this wish"

    def is_available(self) -> bool:
        return self.wish.creator == self.user and self.wish.in_status(
            self.wish.STATUSES.NEW
        )

    def _execute(self, request: HttpRequest):
        self.wish.delete()

    def get_success_url(self):
        return reverse("wizuber:list-wish")


class PayAction(IAction):
    @classmethod
    def get_action_name(cls) -> str:
        return "pay"

    @classmethod
    def get_action_description(cls) -> str:
        return "Pay for this with to make it visible for wizard"

    def is_available(self) -> bool:
        return (
            self.wish.creator == self.user
            and self.wish.status == self.wish.STATUSES.NEW.name
        )

    def _is_processing_available(self) -> bool:
        return self.user.balance >= self.wish.price

    def _execute(self, request: HttpRequest):
        self.user.balance = F("balance") - self.wish.price
        self.user.save()
        self.user.refresh_from_db()
        self.wish.status = self.wish.STATUSES.ACTIVE.name
        self.wish.save()


class OwnAction(IAction):
    @classmethod
    def get_action_name(cls) -> str:
        return "own"

    @classmethod
    def get_action_description(cls) -> str:
        return "You can accept order for this wish"

    def is_available(self) -> bool:
        without_owner = self.wish.owner is None
        is_active_status = self.wish.status == self.wish.STATUSES.ACTIVE.name
        return self.user.is_wizard and without_owner and is_active_status

    def _execute(self, request: HttpRequest):
        self.wish.owner = self.user
        self.wish.assigned_to = self.user
        self.wish.status = self.wish.STATUSES.WORK.name
        self.wish.save()


class ArtifactAction(IAction, ABC):
    """ Abstract class for artifact actions. """

    def is_available(self) -> bool:
        user, wish = self.user, self.wish
        is_work_status = wish.status == wish.STATUSES.WORK.name

        if is_work_status and user.is_wizard and user == wish.owner == wish.assigned_to:
            return True

        if (
            is_work_status
            and user.is_student
            and wish.owner == user.teacher
            and user == wish.assigned_to
        ):
            return True

        return False

    @classmethod
    @abstractmethod
    def get_artifact_name(cls) -> str:
        """ String value of artifact name. Part of action name. """

    @classmethod
    def get_action_name(cls) -> str:
        return f"{cls.get_artifact_name()}-artifact"

    @classmethod
    def get_action_description(cls) -> str:
        return f"Add {cls.get_artifact_name()} artifact for this wish"

    @classmethod
    @abstractmethod
    def get_form_class(cls) -> Type[ModelForm]:
        """ Class of the form used by this artifact action. """

    def get_form(self, request: HttpRequest = None) -> ModelForm:
        cls = self.get_form_class()
        return cls(data=request.POST if request else None)

    def _execute(self, request: HttpRequest):
        form = self.get_form(request)
        form.instance.wish = self.wish
        if not form.is_valid():
            raise ValueError
        form.save()


class CandleArtifactAction(ArtifactAction):
    @classmethod
    def get_artifact_name(cls) -> str:
        return "candle"

    @classmethod
    def get_form_class(cls) -> Type[ModelForm]:
        return CandleArtifactForm


class PentacleArtifactAction(ArtifactAction):
    @classmethod
    def get_artifact_name(cls) -> str:
        return "pentacle"

    @classmethod
    def get_form_class(cls) -> Type[ModelForm]:
        return PentacleArtifactForm


class SpiritArtifactAction(ArtifactAction):
    @classmethod
    def get_artifact_name(cls) -> str:
        return "spirit"

    @classmethod
    def get_form_class(cls) -> Type[ModelForm]:
        return SpiritArtifactForm


class AssignToStudentAction(IAction):
    @classmethod
    def get_action_name(cls) -> str:
        return "to-student"

    @classmethod
    def get_action_description(cls) -> str:
        return "You can assign this wish to your student"

    def is_available(self) -> bool:
        user, wish = self.user, self.wish
        is_work_status = wish.status == wish.STATUSES.WORK.name

        return (
            is_work_status
            and user.is_wizard
            and user == wish.owner == wish.assigned_to
            and user.has_student()
        )

    def _execute(self, request: HttpRequest):
        self.wish.assigned_to = self.user.student
        self.wish.save()


class AssignToWizardAction(IAction):
    @classmethod
    def get_action_name(cls) -> str:
        return "to-wizard"

    @classmethod
    def get_action_description(cls) -> str:
        return "You should assign this wish back to your teacher"

    def is_available(self) -> bool:
        user, wish = self.user, self.wish
        is_work_status = wish.status == wish.STATUSES.WORK.name

        return (
            is_work_status
            and user.is_student
            and wish.owner == user.teacher
            and user == wish.assigned_to
        )

    def _execute(self, request: HttpRequest):
        self.wish.assigned_to = self.user.teacher
        self.wish.save()


class AssignToSpiritAction(IAction):
    @classmethod
    def get_action_name(cls) -> str:
        return "to-spirit"

    @classmethod
    def get_action_description(cls) -> str:
        return "You can assign wish to spirit"

    def is_available(self) -> bool:
        user, wish = self.user, self.wish
        is_work_status = wish.status == wish.STATUSES.WORK.name

        return (
            is_work_status
            and user.is_wizard
            and user == wish.owner == wish.assigned_to
            and wish.has_spirit_artifact()
            and wish.pentacle_artifacts.exists()
        )

    def _execute(self, request: HttpRequest):
        self.wish.assigned_to = self.wish.spirit_artifact.spirit
        self.wish.status = self.wish.STATUSES.ON_SPIRIT.name
        self.wish.save()


class AssignFromSpiritToWizardAction(IAction):
    @classmethod
    def get_action_name(cls) -> str:
        return "spirit-to-wizard"

    @classmethod
    def get_action_description(cls) -> str:
        return "You can assign wish back to wizard"

    def is_available(self) -> bool:
        user, wish = self.user, self.wish
        is_on_spirit_status = wish.status == wish.STATUSES.ON_SPIRIT.name

        return is_on_spirit_status and user.is_spirit and user == wish.assigned_to

    def _execute(self, request: HttpRequest):
        self.wish.assigned_to = self.wish.owner
        self.wish.status = self.wish.STATUSES.READY.name
        self.wish.save()


class CloseAction(IAction):
    @classmethod
    def get_action_name(cls) -> str:
        return "close"

    @classmethod
    def get_action_description(cls) -> str:
        return "You can close this wish"

    def is_available(self) -> bool:
        user, wish = self.user, self.wish
        is_ready = wish.status == wish.STATUSES.READY.name

        return is_ready and user.is_wizard and user == wish.owner == wish.assigned_to

    def _execute(self, request: HttpRequest):
        self.wish.assigned_to = self.wish.creator
        self.wish.status = self.wish.STATUSES.CLOSED.name
        self.wish.save()
        self.user.balance = F("balance") + self.wish.price
        self.user.save()
        self.user.refresh_from_db()
