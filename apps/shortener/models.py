from django.conf import settings
from django.db import models

from rest_framework.exceptions import ValidationError


class ShortenedURL(models.Model):
    long_url = models.CharField(max_length=512)
    suggested_path = models.CharField(max_length=128, blank=True, null=True)
    key = models.CharField(max_length=512, unique=True, blank=True,
                           null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    hits = models.IntegerField(default=0)

    def __str__(self):
        return '%s %s' % (self.long_url, self.short_url)

    def clean(self):
        if not (self.long_url.startswith("http") or
                self.long_url.startswith("https")):
            raise ValidationError('URL should start with "http" or "https"')

    @staticmethod
    def short_url(key):
        return settings.SHORT_URL_DOMAIN + key

    @staticmethod
    def redis_counter_key(key):
        return key + '_' + 'counter'

    def set_on_redis(self, redis_instance):
        redis_instance.set(name=self.key,
                           value=self.long_url)
        redis_instance.set(name=self.redis_counter_key(self.key),
                           value=0)
