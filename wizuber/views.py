from django.shortcuts import render, get_object_or_404
from django.views import generic

from wizuber.models import Wizard


def index(request):
    return render(request, 'wizuber/index.html')


class WizardsView(generic.ListView):
    template_name = 'wizuber/wizards.html'
    context_object_name = 'wizards'

    def get_queryset(self):
        return Wizard.objects.all()


def wizard_detail(request, wizard_id):
    return render(request, 'wizuber/wizard_detail.html', dict(question=get_object_or_404(Wizard, pk=wizard_id)))
