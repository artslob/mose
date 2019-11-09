from django.views import generic

from wizuber.models import Wizard


class ListWizard(generic.ListView):
    template_name = 'wizuber/wizard/list.html'
    context_object_name = 'wizards'

    def get_queryset(self):
        return Wizard.objects.all()


class DetailWizard(generic.DetailView):
    model = Wizard
    template_name = 'wizuber/wizard/detail.html'
