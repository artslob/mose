from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import generic

from wizuber.forms import CustomerSignUpForm
from wizuber.models import Wizard, Wishes


def index(request):
    return render(request, 'wizuber/index.html')


class CustomerSignUp(generic.CreateView):
    form_class = CustomerSignUpForm
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


@method_decorator(permission_required('wizuber.view_wishes'), name='dispatch')
class WishesList(generic.ListView):
    model = Wishes
    context_object_name = 'wishes'
    template_name = 'wizuber/wishes.html'

    def get_queryset(self):
        user = self.request.user
        if user.is_customer():
            return self.model.objects.filter(creator=user.customer)
        if user.is_wizard():
            return self.model.objects.filter(creator=user.wizard)
        return self.model.objects.none()


@method_decorator(permission_required('wizuber.add_wishes'), name='dispatch')
class CreateWish(generic.CreateView):
    # TODO provide wish creator by yourself
    model = Wishes
    fields = ['description', 'creator']
    template_name = 'wizuber/create_wish.html'

    def get_success_url(self):
        return reverse('wizuber:wish_detail', kwargs=dict(pk=self.object.pk))


class WishDetail(generic.DetailView):
    model = Wishes
    context_object_name = 'wish'
    template_name = 'wizuber/wish_detail.html'
