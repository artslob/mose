from pathlib import Path

from django.test import TestCase
from django.urls import reverse

from wizuber.fsm import IAction, action_classes, action_class_by_name, ActionNotFound


class FsmAvailableActions(TestCase):
    def setUp(self):
        self.expected_number_of_actions = 11

    def test_available_actions_length(self):
        method_length = len(action_classes())
        dict_length = len(IAction.defined_actions)
        self.assertTrue(dict_length == method_length == self.expected_number_of_actions)

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
        with self.assertRaises(ActionNotFound) as context:
            action_class_by_name('test')

        error_msg = str(context.exception)
        self.assertTrue("action with name 'test' not found" == error_msg)

    def test_post_action_not_existing_name(self):
        kwargs = dict(pk=1, action='test-action')
        url = reverse('wizuber:handle-wish-action', kwargs=kwargs)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

    def test_action_have_templates(self):
        wizuber_dir: Path = Path(__file__).resolve().parent.parent
        templates_dir = wizuber_dir / 'templates'
        self.assertTrue(templates_dir.is_dir())
        for cls in action_classes():
            template_path = cls.get_full_template_name()
            self.assertTrue(isinstance(template_path, str))
            full_template_path = templates_dir / template_path
            self.assertTrue(full_template_path.is_file(), msg=f'template {template_path!r} not exist')
