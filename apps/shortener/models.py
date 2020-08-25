from django.conf import settings
from django.db import models
from django.utils import timezone

from rest_framework.exceptions import ValidationError


class ShortenedURL(models.Model):
    user = models.ForeignKey('accounts.User', related_name='urls',
                             on_delete=models.CASCADE)
    long_url = models.CharField(max_length=512)
    suggested_path = models.CharField(max_length=32, blank=True, null=True)
    key = models.CharField(max_length=8, unique=True, default='',
                           db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.long_url} {self.key}'

    def clean(self):
        if not (self.long_url.startswith("http") or
                self.long_url.startswith("https")):
            raise ValidationError('URL should start with "http" or "https"')

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


class PlatFormTypes:
    MOBILE = 'mobile'
    TABLET = 'tablet'
    DESKTOP = 'desktop'

    TYPES = (
        (MOBILE, MOBILE),
        (TABLET, TABLET),
        (DESKTOP, DESKTOP),
    )


class Analytic(models.Model):
    short_url = models.OneToOneField('ShortenedURL', related_name='analytic',
                                     on_delete=models.CASCADE)

    all_visits = models.JSONField(default=dict)
    unique_visits = models.JSONField(default=dict)

    def _update(self, uniques=False):
        queryset = self.short_url.visits.all()
        if uniques:
            queryset = queryset.distinct('session_key')

        queries = self.time_separate_queryset(queryset)

        for date_field in self.date_fields():
            # Total visits
            self.all_visits['total'][date_field] = queries[date_field].count()

            # Platform specific visits
            self.all_visits['platform'][date_field] = queries[
                date_field].values('platform').order_by().annotate(
                models.Count('platform'))

            # Browser specific visits
            self.all_visits['browser'][date_field] = queries[
                date_field].values('browser').order_by().annotate(
                models.Count('browser'))

    def update_analytic(self):
        self._update(uniques=False)
        self._update(uniques=True)
        self.save()

    def time_separate_queryset(self, queryset: models.QuerySet,
                               apply_count=False):
        today_t = self.date_range()
        yesterday_t = self.date_range(days=1)
        last_week_t = self.date_range(days=7)
        last_month_t = self.date_range(days=30)

        always = queryset
        today = queryset.filter(created_at__gte=today_t)
        yesterday = queryset.filter(created_at__gte=yesterday_t[0],
                                    created_at__ls=yesterday_t[1])
        last_week = queryset.filter(created_at__gte=last_week_t[0],
                                    created_at__ls=last_week_t[1])
        last_month = queryset.filter(created_at__gte=last_month_t[0],
                                     created_at_ls=last_month_t[1])

        queries = {'always': always, 'today': today,
                   'yesterday': yesterday,
                   'last_week': last_week,
                   'last_month': last_month}

        if apply_count:
            queries = {k: v.count() for k, v in queries.items()}

        return queries

    @staticmethod
    def date_range(days=0):
        now = timezone.now().date()
        if days:
            lower_bound = now - timezone.timedelta(days=days)
            return lower_bound, now
        return now

    @staticmethod
    def date_fields():
        return 'always', 'today', 'yesterday', 'last_week', 'last_month'

    def __str__(self):
        return self.short_url.__str__()


class Visit(models.Model):
    short_url = models.ForeignKey('ShortenedURL', related_name='visits',
                                  on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True, db_index=True)
    platform = models.CharField(max_length=16, choices=PlatFormTypes.TYPES,
                                db_index=True)
    browser = models.CharField(max_length=128, db_index=True)
    session_key = models.CharField(max_length=64, db_index=True)
