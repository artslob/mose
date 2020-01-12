from django.apps import AppConfig
from django.db.models.signals import post_migrate, post_save

from wizuber.const import WIZARD_PERM, CUSTOMER_PERM, CUSTOMER_GROUP, WIZARD_GROUP


class WizuberConfig(AppConfig):
    name = "wizuber"

    def ready(self):
        """
        This code creates default groups for some types of users and assigns these groups to specific types of users
        when they are created.
        This idea using Django permission framework for access control Wizuber was abandoned because of superusers
        have all permissions, so its requires extra check to distinguish superuser from customer or wizard for example.
        Code is left for future reference.
        """
        post_migrate.connect(populate_models, sender=self)

        from wizuber.models import Wizard, Customer

        for model in (Wizard, Customer):
            post_save.connect(add_to_default_group, sender=model)


def add_to_default_group(sender, **kwargs):
    if not kwargs["created"]:
        return

    from django.contrib.auth.models import Group
    from wizuber.models import Wizard, Customer

    model_to_group_name = {
        Wizard: WIZARD_GROUP,
        Customer: CUSTOMER_GROUP,
    }

    group_name = model_to_group_name[sender]

    user = kwargs["instance"]
    user.groups.add(Group.objects.get(name=group_name))


def populate_models(sender, **kwargs):
    from django.contrib.auth.models import Group, Permission

    app = dict(content_type__app_label="wizuber")
    # models
    rights = dict(content_type__model="rightssupport")
    wishes = dict(content_type__model="wish")

    customer_group, created = Group.objects.get_or_create(name=CUSTOMER_GROUP)
    customer_group.permissions.add(
        Permission.objects.get(codename=CUSTOMER_PERM, **app, **rights),
        Permission.objects.get(codename="add_wish", **app, **wishes),
        Permission.objects.get(codename="view_wish", **app, **wishes),
        Permission.objects.get(codename="change_wish", **app, **wishes),
    )

    wizard_group, created = Group.objects.get_or_create(name=WIZARD_GROUP)
    wizard_group.permissions.add(
        Permission.objects.get(codename=WIZARD_PERM, **app, **rights),
        Permission.objects.get(codename="view_wish", **app, **wishes),
        Permission.objects.get(codename="change_wish", **app, **wishes),
    )
