from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.views import generic

from wizuber.models import Wizard, Wish, is_wizard
from wizuber.views.helpers import PageTitleMixin


# TODO add checks for permissions


class ListWish(LoginRequiredMixin, PageTitleMixin, generic.ListView):
    """
    Returns list of wishes. For specific types of users returns different results:
    Customer: wishes created by him;
    Wizard: wishes owned by him;
    Student: wishes assigned to him;
    Spirit: wishes assigned to him;
    """
    page_title = 'Wishes List'
    model = Wish
    context_object_name = 'wishes'
    template_name = 'wizuber/wish/list.html'

    def get_queryset(self):
        return self.request.user.get_queryset_for_wish_list()


class ListWishActive(UserPassesTestMixin, ListWish):
    """ Returns wish list for wizard (only with "active" status). Represents "new orders" page. """
    page_title = 'Available Wishes For Order'

    def test_func(self):
        return is_wizard(self.request.user)

    def get_queryset(self):
        return Wish.objects.filter(status=Wish.STATUSES.ACTIVE.name)


class CreateWish(LoginRequiredMixin, UserPassesTestMixin, PageTitleMixin, generic.CreateView):
    page_title = 'Create New Wish'
    model = Wish
    fields = ['description']
    template_name = 'wizuber/wish/create.html'

    def test_func(self):
        return self.request.user.can_create_wish

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class DetailWish(LoginRequiredMixin, PageTitleMixin, generic.DetailView):
    page_title = 'Wish Details'
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
        return redirect(wish.get_absolute_url())
