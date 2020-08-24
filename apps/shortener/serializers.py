from rest_framework import serializers

from .models import ShortenedURL


class ShortenedURLSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('source', 'suggested_path', 'destination',
                  'hits')

        extra_kwargs = {
            'destination': {'read_only': True},
            'hits': {'read_only': True}
        }
