from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group

from wizuber.models import WizuberUser, Customer


class WizuberUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = WizuberUser
        fields = '__all__'


class WizuberUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = WizuberUser
        fields = '__all__'


class CustomerSignUpForm(UserCreationForm):
    required_css_class = 'required-label-asterisk'

    class Meta(UserCreationForm.Meta):
        model = WizuberUser
        fields = ('username', 'email', 'first_name', 'last_name', 'middle_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=True)
        Customer.objects.create(profile=user)
        user.groups.add(Group.objects.get(name='customer'))
        return user
