from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from wizuber.forms import WizuberUserCreationForm, WizuberUserChangeForm
from wizuber.models import Wizard, WizuberUser


class WizuberUserModelAdmin(UserAdmin):
    add_form = WizuberUserCreationForm
    form = WizuberUserChangeForm
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            'fields': ('email', 'first_name', 'last_name', 'middle_name', 'is_staff', 'is_active', 'is_superuser')
        }),
    )


admin.site.register(WizuberUser, WizuberUserModelAdmin)
admin.site.register(Wizard, WizuberUserModelAdmin)
