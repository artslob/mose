from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from wizuber.forms import WizuberUserCreationForm, WizuberUserChangeForm
from wizuber.models import Wizard, WizuberUser


class CustomUserAdmin(UserAdmin):
    add_form = WizuberUserCreationForm
    form = WizuberUserChangeForm
    model = WizuberUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', ]
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser')}
         ),
    )
    ordering = ('username',)


admin.site.register(WizuberUser, CustomUserAdmin)
admin.site.register(Wizard)
