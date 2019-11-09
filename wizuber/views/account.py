from django.urls import reverse_lazy
from django.views import generic

from wizuber.forms import CustomerSignUpForm


class CustomerSignUp(generic.CreateView):
    form_class = CustomerSignUpForm
    success_url = reverse_lazy('wizuber:index')
    template_name = 'wizuber/account/signup.html'
