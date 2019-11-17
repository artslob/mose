from django.test import TestCase, Client

from wizuber.fsm import IAction, ActionMapping


class FsmAvailableActions(TestCase):
    def setUp(self):
        self.expected_number_of_actions = 2

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

    def test_get_action_class_by_not_existing_name(self):
        self.assertRaises(KeyError, ActionMapping.action_class_by_name, 'test-action')

    def test_post_action_not_existing_name(self):
        response = Client().post('wish/1/handle/test-action')
        self.assertEqual(response.status_code, 404)
