from django.test import TestCase, Client

from wizuber.fsm import IAction, action_classes, action_class_by_name


class FsmAvailableActions(TestCase):
    def setUp(self):
        self.expected_number_of_actions = 3

    def test_available_actions_length(self):
        enum_length = len(action_classes())
        dict_length = len(IAction.defined_actions)
        self.assertTrue(dict_length == enum_length == self.expected_number_of_actions)

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
        for cls in action_classes():
            self.assertTrue(issubclass(cls, IAction))

    def test_get_action_class_by_name(self):
        for name in ('delete', 'own', 'pay'):
            cls = action_class_by_name(name)
            self.assertTrue(issubclass(cls, IAction))

    def test_get_action_class_by_not_existing_name(self):
        self.assertRaises(KeyError, action_class_by_name, 'test-action')

    def test_post_action_not_existing_name(self):
        response = Client().post('wish/1/handle/test-action')
        self.assertEqual(response.status_code, 404)
