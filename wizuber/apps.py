from django.apps import AppConfig
from django.db.models.signals import post_migrate


class WizuberConfig(AppConfig):
    name = 'wizuber'

    def ready(self):
        post_migrate.connect(populate_models, sender=self)


def populate_models(sender, **kwargs):
    from django.contrib.auth.models import Group, Permission

    app = dict(content_type__app_label='wizuber')
    # models
    rights = dict(content_type__model='rightssupport')
    wishes = dict(content_type__model='wishes')

    customer_group, created = Group.objects.get_or_create(name='customer')
    customer_group.permissions.add(
        Permission.objects.get(codename='customer_rights', **app, **rights),
        Permission.objects.get(codename='view_wishes', **app, **wishes),
        Permission.objects.get(codename='add_wishes', **app, **wishes),
        Permission.objects.get(codename='change_wishes', **app, **wishes),
    )

    wizard_group, created = Group.objects.get_or_create(name='wizard')
    wizard_group.permissions.add(
        Permission.objects.get(codename='wizard_rights', **app, **rights),
        Permission.objects.get(codename='view_wishes', **app, **wishes),
        Permission.objects.get(codename='change_wishes', **app, **wishes),
    )
