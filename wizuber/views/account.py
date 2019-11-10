from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView

from wizuber.forms import CustomerSignUpForm
from wizuber.views.helpers import PageTitleMixin


class DetailAccount(LoginRequiredMixin, PageTitleMixin, TemplateView):
    template_name = 'wizuber/account/detail.html'
    page_title = 'Account'


class LoginAccount(PageTitleMixin, LoginView):
    template_name = 'wizuber/account/login.html'
    page_title = 'Login'


class CustomerSignUp(PageTitleMixin, generic.CreateView):
    form_class = CustomerSignUpForm
    success_url = reverse_lazy('wizuber:index')
    template_name = 'wizuber/account/signup.html'

    page_title = 'Sign up'
