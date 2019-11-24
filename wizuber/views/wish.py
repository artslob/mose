from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden, Http404, HttpRequest
from django.shortcuts import redirect
from django.views import generic

from wizuber.fsm import action_classes, action_class_by_name, ActionNotFound, ActionAccessDenied
from wizuber.models import Wizard, Wish
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
        return self.request.user.is_wizard

    def get_queryset(self):
        return Wish.objects.filter(status=Wish.STATUSES.ACTIVE.name)


class ListWishClosed(ListWishActive):
    """ Returns customer`s wish list with closed statuses. """
    page_title = 'Closed Wishes'

    def test_func(self):
        return self.request.user.is_customer

    def get_queryset(self):
        return Wish.objects.filter(status=Wish.STATUSES.CLOSED.name, creator=self.request.user)


class CreateWish(LoginRequiredMixin, UserPassesTestMixin, PageTitleMixin, generic.CreateView):
    page_title = 'Create New Wish'
    model = Wish
    fields = ['description', 'price']
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['actions'] = self.get_actions()
        return context

    def get_actions(self):
        wish, user = self.object, self.request.user
        action_instances = (cls(wish, user) for cls in action_classes())
        return [action for action in action_instances if action.is_available()]


class HandleWishAction(LoginRequiredMixin, generic.View, generic.detail.SingleObjectMixin):
    model = Wish

    def post(self, request: HttpRequest, pk: int, action: str):
        print(pk, action)
        try:
            action_class = action_class_by_name(action)
        except ActionNotFound:
            raise Http404
        print(action_class)
        action = action_class(wish=self.get_object(), user=self.request.user)
        try:
            action.execute(request)
        except ActionAccessDenied:
            raise PermissionDenied from None
        return redirect(action.get_success_url())


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
