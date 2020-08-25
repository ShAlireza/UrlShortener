from django.conf import settings
from django.db import models
from django.utils import timezone

from rest_framework.exceptions import ValidationError


class ShortenedURL(models.Model):
    """
    Model for create new shortened url for users. 
    """
    user = models.ForeignKey('accounts.User', related_name='urls',
                             on_delete=models.CASCADE)
    long_url = models.URLField(max_length=512)
    suggested_path = models.CharField(max_length=32, blank=True, null=True)
    key = models.CharField(max_length=8, unique=True, default='',
                           db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.long_url} {self.key}'

    @property
    def hits(self):
        return self.visits.count()

    def short_url(self):
        if self.suggested_path:
            return (settings.SHORT_URL_DOMAIN + self.key +
                    '-' + self.suggested_path)
        return settings.SHORT_URL_DOMAIN + self.key

    def set_on_redis(self, redis_instance):
        redis_instance.set(name=self.key,
                           value=self.long_url)


class Analytic(models.Model):
    short_url = models.OneToOneField('ShortenedURL', related_name='analytic',
                                     on_delete=models.CASCADE)

    all_visits = models.JSONField(default=dict)
    unique_visits = models.JSONField(default=dict)

    @classmethod
    def create_new(cls, short_url):
        """
        Helper function for create a new instance of Analytic with default
        dictionaries for all_visits and unique_visits fields.
        :param short_url: 
        :return: Analytic
        """
        default = {'total': {}, 'platform': {}, 'browser': {}}
        return cls.objects.create(short_url=short_url, all_visits=default,
                                  unique_visits=default.copy())

    def _update(self, uniques=False):
        """
        Do update stuff needed for analytic fields
        :param uniques: 
        """
        queryset = self.short_url.visits.all()
        field = self.all_visits
        if uniques:
            ids = queryset.distinct('session_key').values_list('id',
                                                               flat=True)
            queryset = self.short_url.visits.filter(id__in=ids)
            field = self.unique_visits

        # Get query for each date range needed
        queries = self.time_separate_queryset(queryset)

        for date_field in self.date_fields():
            # Total visits
            field['total'][date_field] = queries[date_field].count()

            # Platform specific visits
            field['platform'][date_field] = list(queries[
                date_field].values('platform').order_by().annotate(
                models.Count('platform')))

            # Browser specific visits
            field['browser'][date_field] = list(queries[
                date_field].values('browser').order_by().annotate(
                models.Count('browser')))

    def update_analytic(self):
        """
        Helper method for updating both kind of analytics, all and unique 
        """
        self._update(uniques=False)
        self._update(uniques=True)
        self.save()

    def time_separate_queryset(self, queryset: models.QuerySet):
        """
        Create 4 new distinct querysets from base queryset according to 
        4 different date ranges: today, yesterday, last week and last month
        :param queryset: 
        :return: Dict[str, models.Queryset]
        """
        today_t = self.date_range()
        yesterday_t = self.date_range(days=1)
        last_week_t = self.date_range(days=7)
        last_month_t = self.date_range(days=30)

        today = queryset.filter(created_at__gte=today_t)
        yesterday = queryset.filter(created_at__gte=yesterday_t[0],
                                    created_at__lt=yesterday_t[1])
        last_week = queryset.filter(created_at__gte=last_week_t[0],
                                    created_at__lt=last_week_t[1])
        last_month = queryset.filter(created_at__gte=last_month_t[0],
                                     created_at__lt=last_month_t[1])

        queries = {'today': today,
                   'yesterday': yesterday,
                   'last_week': last_week,
                   'last_month': last_month}

        return queries

    @staticmethod
    def date_range(days=0):
        """
        Generate a lower bound for now minus given days
        :param days: 
        :return: Union[datetime.date, Tuple[datetime.date]]:
        a single date if days = 0 otherwise a tuple
        """
        now = timezone.now().date()
        if days:
            lower_bound = now - timezone.timedelta(days=days)
            return lower_bound, now
        return now

    @staticmethod
    def date_fields():
        """
        Get date field names used in json responses
        :return: Tuple[str]
        """
        return 'today', 'yesterday', 'last_week', 'last_month'

    def __str__(self):
        return self.short_url.__str__()


class PlatFormTypes:
    """
    Helper class just used as enum for different kinds of platforms
    """
    MOBILE = 'mobile'
    TABLET = 'tablet'
    DESKTOP = 'desktop'

    TYPES = (
        (MOBILE, MOBILE),
        (TABLET, TABLET),
        (DESKTOP, DESKTOP),
    )


class Visit(models.Model):
    short_url = models.ForeignKey('ShortenedURL', related_name='visits',
                                  on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True, db_index=True)
    platform = models.CharField(max_length=16, choices=PlatFormTypes.TYPES,
                                db_index=True)
    browser = models.CharField(max_length=128, db_index=True)
    session_key = models.CharField(max_length=64, db_index=True)
