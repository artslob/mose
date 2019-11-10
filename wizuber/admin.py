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
    personal_info = ('Personal info', {'fields': ('email', 'first_name', 'last_name', 'middle_name')})
    add_fieldsets = UserAdmin.add_fieldsets + (personal_info,)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        personal_info,
    )


class WizardModelAdmin(WizuberUserModelAdmin):
    add_form = create_user_admin_form(Wizard, UserCreationForm)
    form = create_user_admin_form(Wizard, UserChangeForm)


class StudentModelAdmin(WizuberUserModelAdmin):
    add_form = create_user_admin_form(Student, UserCreationForm)
    form = create_user_admin_form(Student, UserChangeForm)
    addition_fields = ('Additional fields', {'fields': ('teacher',)})
    add_fieldsets = WizuberUserModelAdmin.add_fieldsets + (addition_fields,)
    fieldsets = WizuberUserModelAdmin.fieldsets + (addition_fields,)


class SpiritModelAdmin(WizuberUserModelAdmin):
    add_form = create_user_admin_form(Spirit, UserCreationForm)
    form = create_user_admin_form(Spirit, UserChangeForm)
    addition_fields = ('Additional fields', {'fields': ('grade', 'master')})
    add_fieldsets = WizuberUserModelAdmin.add_fieldsets + (addition_fields,)
    fieldsets = WizuberUserModelAdmin.fieldsets + (addition_fields,)


admin.site.register(WizuberUser, WizuberUserModelAdmin)
admin.site.register(Wizard, WizardModelAdmin)
admin.site.register(Student, StudentModelAdmin)
admin.site.register(Spirit, SpiritModelAdmin)
