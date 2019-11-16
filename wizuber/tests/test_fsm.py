from django.test import TestCase

from wizuber.fsm import IAction


class FsmAvailableActions(TestCase):
    def test_available_actions_length(self):
        self.assertTrue(len(IAction.defined_actions) == 1)
