from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic

from wizuber.models import Wizard, Wish, is_wizard


# TODO add checks for permissions

class ListWish(LoginRequiredMixin, generic.ListView):
    model = Wish
    context_object_name = 'wishes'
    template_name = 'wizuber/wish/list.html'

    def get_queryset(self):
        return self.request.user.get_queryset_for_wish_list(self.model)


class ListWishActive(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model = Wish
    context_object_name = 'wishes'
    template_name = 'wizuber/wish/list.html'

    def test_func(self):
        return is_wizard(self.request.user)

    def get_queryset(self):
        return Wish.objects.filter(status=Wish.STATUSES.ACTIVE.name).all()


class CreateWish(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Wish
    fields = ['description']
    template_name = 'wizuber/wish/create.html'

    def test_func(self):
        return self.request.user.can_create_wish

    def get_success_url(self):
        return reverse('wizuber:detail-wish', kwargs=dict(pk=self.object.pk))

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class DetailWish(LoginRequiredMixin, generic.DetailView):
    model = Wish
    context_object_name = 'wish'
    template_name = 'wizuber/wish/detail.html'


class FulfillWish(LoginRequiredMixin, generic.View, generic.detail.SingleObjectMixin):
    model = Wish

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
