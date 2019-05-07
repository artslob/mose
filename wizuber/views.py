from django.shortcuts import render
from django.views import generic

from wizuber.models import Wizard


def index(request):
    return render(request, 'wizuber/index.html')


class WizardsView(generic.ListView):
    template_name = 'wizuber/wizards.html'
    context_object_name = 'wizards'

    def get_queryset(self):
        return Wizard.objects.all()


class WizardDetail(generic.DetailView):
    model = Wizard
    template_name = 'wizuber/wizard_detail.html'
