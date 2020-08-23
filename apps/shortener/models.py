from django.db import models

from rest_framework.exceptions import ValidationError


class ShortenedUrl(models.Model):
    source = models.CharField(max_length=512)
    destination = models.CharField(max_length=512, blank=True, null=True,
                                   unique=True)
    hits = models.IntegerField(default=0)

    def __str__(self):
        return '%s %s' % (self.source, self.destination)

    def clean(self):
        if not (self.destination.startswith("http") or
                self.destination.startswith("https")):
            raise ValidationError('URL should start with "http" or "https"')
