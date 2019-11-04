from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from wizuber.models import WizuberUser, Wizard, Student, Spirit


def create_user_admin_form(form_model, base_class, model_fields='__all__'):
    class DynamicUserAdminForm(base_class):
        class Meta(base_class.Meta):
            model = form_model
            fields = model_fields

    return DynamicUserAdminForm


class WizuberUserModelAdmin(UserAdmin):
    add_form = create_user_admin_form(WizuberUser, UserCreationForm)
    form = create_user_admin_form(WizuberUser, UserChangeForm)
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            'fields': ('email', 'first_name', 'last_name', 'middle_name', 'is_staff', 'is_active', 'is_superuser')
        }),
    )


class WizardModelAdmin(WizuberUserModelAdmin):
    add_form = create_user_admin_form(Wizard, UserCreationForm)
    form = create_user_admin_form(Wizard, UserCreationForm)


class StudentModelAdmin(WizuberUserModelAdmin):
    add_form = create_user_admin_form(Student, UserCreationForm)
    form = create_user_admin_form(Student, UserCreationForm)


class SpiritModelAdmin(WizuberUserModelAdmin):
    add_form = create_user_admin_form(Spirit, UserCreationForm)
    form = create_user_admin_form(Spirit, UserCreationForm)
    add_fieldsets = WizuberUserModelAdmin.add_fieldsets + (
        (None, {'fields': ('grade',)}),
    )


admin.site.register(WizuberUser, WizuberUserModelAdmin)
admin.site.register(Wizard, WizardModelAdmin)
admin.site.register(Student, StudentModelAdmin)
admin.site.register(Spirit, SpiritModelAdmin)
