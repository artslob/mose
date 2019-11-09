from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin, LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic

from wizuber.models import Wizard, Wishes


class ListWish(PermissionRequiredMixin, generic.ListView):
    permission_required = 'wizuber.view_wishes'

    model = Wishes
    context_object_name = 'wishes'
    template_name = 'wizuber/wish/list.html'

    def get_queryset(self):
        return self.request.user.get_queryset_for_wish_list(self.model)


class CreateWish(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, generic.CreateView):
    permission_required = 'wizuber.add_wishes'

    model = Wishes
    fields = ['description']
    template_name = 'wizuber/wish/create.html'

    def test_func(self):
        return self.request.user.can_create_wish

    def get_success_url(self):
        return reverse('detail-wish', kwargs=dict(pk=self.object.pk))

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class DetailWish(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'wizuber.view_wishes'

    model = Wishes
    context_object_name = 'wish'
    template_name = 'wizuber/wish/detail.html'


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
        return redirect('detail-wish', pk=pk)
