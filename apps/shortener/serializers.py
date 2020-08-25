from rest_framework import serializers

from .models import ShortenedURL, Analytic
from .services import ShortenedURLService


class AnalyticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analytic
        fields = ('all_visits', 'unique_visits')


class ShortenedURLSerializer(serializers.ModelSerializer):
    analytic = AnalyticSerializer(read_only=True)

    class Meta:
        model = ShortenedURL
        fields = ('long_url', 'suggested_path', 'key', 'hits', 'analytic')

        extra_kwargs = {
            'key': {'read_only': True},
            'hits': {'read_only': True},
        }

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        obj = super().create(validated_data)
        obj.key = ShortenedURLService.id_to_short_url(obj)
        obj.save()
        Analytic.objects.create(short_url=obj)
        return obj
