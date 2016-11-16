import os

from django.views.generic.dates import (
    ArchiveIndexView, DateDetailView, DayArchiveView, MonthArchiveView,
    YearArchiveView,
)

from .models import Entry
from . import config, theme


class BlogViewMixin(object):

    date_field = 'pub_date'
    paginate_by = 10

    def get_allow_future(self):
        return self.request.user.is_staff

    def get_queryset(self):
        if self.request.user.is_staff:
            return Entry.objects.all()
        else:
            return Entry.objects.published()

    def get_context_data(self, **kwargs):
        context = super(BlogViewMixin, self).get_context_data(**kwargs)

        if self.is_post() and theme['sidebar_behavior'] < 3 and theme['clear_reading']:
            theme['sidebar_behavior'] += 3
        context.update(theme=theme, config=config)

        return context

    @staticmethod
    def is_post():
        return False


class BlogArchiveIndexView(BlogViewMixin, ArchiveIndexView):
    def get_template_names(self):
        names = super(BlogArchiveIndexView, self).get_template_names()
        names.append(os.path.join('themes', config['theme'], 'layout', 'index.html'))
        return names


class BlogYearArchiveView(BlogViewMixin, YearArchiveView):
    make_object_list = True


class BlogMonthArchiveView(BlogViewMixin, MonthArchiveView):
    pass


class BlogDayArchiveView(BlogViewMixin, DayArchiveView):
    pass


class BlogDateDetailView(BlogViewMixin, DateDetailView):
    @staticmethod
    def is_post():
        return True
