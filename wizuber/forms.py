from django.contrib.auth.forms import UserCreationForm, UserChangeForm

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
        model = Customer
        fields = ('username', 'email', 'first_name', 'last_name', 'middle_name', 'password1', 'password2')
