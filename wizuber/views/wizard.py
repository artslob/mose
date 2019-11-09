from django.views import generic

from wizuber.models import Wizard


class WizardsView(generic.ListView):
    template_name = 'wizuber/wizard/list.html'
    context_object_name = 'wizards'

    def get_queryset(self):
        return Wizard.objects.all()


class WizardDetail(generic.DetailView):
    model = Wizard
    template_name = 'wizuber/wizard/detail.html'
