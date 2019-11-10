from django.views import generic

from wizuber.models import Wizard
from wizuber.views.helpers import PageTitleMixin


class ListWizard(PageTitleMixin, generic.ListView):
    template_name = 'wizuber/wizard/list.html'
    context_object_name = 'wizards'
    page_title = 'Wizard List'

    def get_queryset(self):
        return Wizard.objects.all()


class DetailWizard(PageTitleMixin, generic.DetailView):
    model = Wizard
    template_name = 'wizuber/wizard/detail.html'
    page_title = 'Wizard Details'
