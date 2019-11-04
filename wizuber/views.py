from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin, LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from wizuber.forms import CustomerSignUpForm
from wizuber.models import Wizard, Wishes


def index(request):
    return render(request, 'wizuber/index.html')


class CustomerSignUp(generic.CreateView):
    form_class = CustomerSignUpForm
    success_url = reverse_lazy('wizuber:index')
    template_name = 'wizuber/account/signup.html'


class WizardsView(generic.ListView):
    template_name = 'wizuber/wizards.html'
    context_object_name = 'wizards'

    def get_queryset(self):
        return Wizard.objects.all()


class WizardDetail(generic.DetailView):
    model = Wizard
    template_name = 'wizuber/wizard_detail.html'


class WishesList(PermissionRequiredMixin, generic.ListView):
    permission_required = 'wizuber.view_wishes'

    model = Wishes
    context_object_name = 'wishes'
    template_name = 'wizuber/wishes.html'

    def get_queryset(self):
        return self.request.user.get_queryset_for_wish_list(self.model)


class CreateWish(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, generic.CreateView):
    permission_required = 'wizuber.add_wishes'

    model = Wishes
    fields = ['description']
    template_name = 'wizuber/create_wish.html'

    def test_func(self):
        return self.request.user.can_create_wish

    def get_success_url(self):
        return reverse('wizuber:wish_detail', kwargs=dict(pk=self.object.pk))

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class WishDetail(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'wizuber.view_wishes'

    model = Wishes
    context_object_name = 'wish'
    template_name = 'wizuber/wish_detail.html'


class FulfillWish(PermissionRequiredMixin, generic.View, generic.detail.SingleObjectMixin):
    permission_required = 'wizuber.change_wishes'

    model = Wishes

    def post(self, request, pk):
        user = request.user
        if not isinstance(user, Wizard):
            return HttpResponseForbidden()
        wish = self.get_object()
        if wish.owner != user:
            return HttpResponseForbidden()
        wish.status = wish.STATUSES.READY.name
        wish.save()
        return redirect('wizuber:wish_detail', pk=pk)
