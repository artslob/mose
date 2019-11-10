from django.views.generic.base import ContextMixin


class PageTitleMixin(ContextMixin):
    page_title = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.page_title:
            context['page_title'] = self.page_title
        return context
