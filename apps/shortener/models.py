from django.conf import settings
from django.db import models

from rest_framework.exceptions import ValidationError


class ShortenedURL(models.Model):
    long_url = models.CharField(max_length=512)
    suggested_path = models.CharField(max_length=128, blank=True, null=True)
    key = models.CharField(max_length=512, unique=True, blank=True,
                           null=True)

    hits = models.IntegerField(default=0)

    def __str__(self):
        return '%s %s' % (self.long_url, self.short_url)

    def clean(self):
        if not (self.long_url.startswith("http") or
                self.long_url.startswith("https")):
            raise ValidationError('URL should start with "http" or "https"')

    @property
    def short_url(self):
        return settings.SHORT_URL_DOMAIN + self.key

    @property
    def redis_counter_key(self):
        return self.short_url + '_' + 'counter'
