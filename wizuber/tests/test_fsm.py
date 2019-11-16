from django.test import TestCase

from wizuber.fsm import IAction, ActionMapping


class FsmAvailableActions(TestCase):
    def setUp(self):
        self.expected_number_of_actions = 1

    def test_available_actions_length(self):
        enum_length = len(ActionMapping.__members__)
        dict_length = len(IAction.defined_actions)
        self.assertTrue(dict_length == enum_length == self.expected_number_of_actions)

    def test_types_of_action_mapping(self):
        for member in ActionMapping:
            self.assertTrue(issubclass(member.value, IAction))

    def test_types_of_defined_action(self):
        defined_actions = IAction.defined_actions
        self.assertTrue(isinstance(defined_actions, dict))
        for key, value in defined_actions.items():
            self.assertTrue(isinstance(key, str))
            self.assertTrue(issubclass(value, IAction))

    def test_unique_defined_actions(self):
        defined_actions = IAction.defined_actions
        keys_unique = len(defined_actions.keys()) == len(set(defined_actions.keys()))
        values_unique = len(defined_actions.values()) == len(set(defined_actions.values()))
        self.assertTrue(keys_unique)
        self.assertTrue(values_unique)

    def test_action_classes_method(self):
        for cls in ActionMapping.action_classes():
            self.assertTrue(issubclass(cls, IAction))

    def test_get_action_class_by_name(self):
        cls = ActionMapping.action_class_by_name('delete')
        self.assertTrue(issubclass(cls, IAction))
