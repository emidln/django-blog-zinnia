"""Mixins for Zinnia archive views"""
from datetime import datetime

from zinnia.settings import PAGINATION
from zinnia.settings import ALLOW_EMPTY
from zinnia.settings import ALLOW_FUTURE


class ArchiveMixin(object):
    """Mixin centralizing the configuration
    of the archives views"""
    paginate_by = PAGINATION
    allow_empty = ALLOW_EMPTY
    allow_future = ALLOW_FUTURE
    date_field = 'creation_date'
    month_format = '%m'
    week_format = '%W'


class PreviousNextPublishedMixin(object):
    """Mixin for correcting the previous/next
    context variable to return dates with published datas"""

    def get_previous_next_published(self, date, period, previous=True):
        """Return the next or previous published date period with Entries"""
        dates = list(self.get_queryset().dates(
            'creation_date', period,
            order=previous and 'ASC' or 'DESC'))
        try:
            index = dates.index(date)
        except ValueError:
            if previous and dates:
                return dates[-1].date()
            else:
                return None
        if index == 0:
            return None
        return dates[index - 1].date()

    def get_next_month(self, date):
        """Get the next month with published Entries"""
        return self.get_previous_next_published(
            datetime(date.year, date.month, 1), 'month',
            previous=False)

    def get_previous_month(self, date):
        """Get the previous month with published Entries"""
        return self.get_previous_next_published(
            datetime(date.year, date.month, 1), 'month',
            previous=True)

    def get_next_day(self, date):
        """Get the next day with published Entries"""
        return self.get_previous_next_published(
            datetime(date.year, date.month, date.day),
            'day', previous=False)

    def get_previous_day(self, date):
        """Get the previous day with published Entries"""
        return self.get_previous_next_published(
            datetime(date.year, date.month, date.day),
            'day', previous=True)
