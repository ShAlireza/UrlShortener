from rest_framework import serializers

from .models import ShortenedURL
from .services import ShortenedURLService


class ShortenedURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortenedURL
        fields = ('source', 'suggested_path', 'destination',
                  'hits')

        extra_kwargs = {
            'destination': {'read_only': True},
            'hits': {'read_only': True}
        }

    def create(self, validated_data):
        obj = super().create(validated_data)
        obj.key = ShortenedURLService.id_to_short_url(obj.id)

        obj.save()
        return obj