from rest_framework import serializers

from .models import ShortenedURL, Analytic
from .services import ShortenedURLService


class AnalyticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analytic
        fields = ('all_visits', 'unique_visits')


class ShortenedURLSerializer(serializers.ModelSerializer):
    analytic = AnalyticSerializer(read_only=True)
    short_url = serializers.SerializerMethodField('_short_url')

    @staticmethod
    def _short_url(obj: ShortenedURL):
        return obj.short_url()

    class Meta:
        model = ShortenedURL
        fields = ('long_url', 'short_url', 'suggested_path', 'key',
                  'analytic')

        extra_kwargs = {
            'key': {'read_only': True},
            'hits': {'read_only': True},
        }

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        obj = super().create(validated_data)
        obj.key = ShortenedURLService.id_to_short_url(obj)
        obj.save()
        Analytic.create_new(short_url=obj)
        return obj
