from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from wizuber.models import Wizard


def index(request):
    return render(request, 'wizuber/index.html')


class CustomerSignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('wizuber:index')
    template_name = 'wizuber/signup.html'


class WizardsView(generic.ListView):
    template_name = 'wizuber/wizards.html'
    context_object_name = 'wizards'

    def get_queryset(self):
        return Wizard.objects.all()


class WizardDetail(generic.DetailView):
    model = Wizard
    template_name = 'wizuber/wizard_detail.html'
