from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import WizuberUser


class WizuberUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = WizuberUser
        fields = '__all__'


class WizuberUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = WizuberUser
        fields = '__all__'
