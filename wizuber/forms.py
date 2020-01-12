from django.contrib.auth.forms import UserCreationForm

from wizuber.models import Customer


class CustomerSignUpForm(UserCreationForm):
    required_css_class = "required-label-asterisk"

    class Meta(UserCreationForm.Meta):
        model = Customer
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "middle_name",
            "password1",
            "password2",
        )
