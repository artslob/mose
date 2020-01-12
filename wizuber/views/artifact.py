from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DeleteView

from wizuber.models import BaseArtifact


class DeleteArtifact(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BaseArtifact

    http_method_names = ["post", "delete", "head", "options", "trace"]

    def test_func(self):
        user, wish = self.request.user, self.get_object().wish
        is_work_status = wish.status == wish.STATUSES.WORK.name

        if is_work_status and user.is_wizard and user == wish.owner == wish.assigned_to:
            return True

        if (
            is_work_status
            and user.is_student
            and wish.owner == user.teacher
            and user == wish.assigned_to
        ):
            return True

        return False

    def get_success_url(self):
        return self.object.wish.get_absolute_url()
