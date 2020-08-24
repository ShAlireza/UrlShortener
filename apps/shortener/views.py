import redis

from django.conf import settings

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from .serializers import ShortenedURLSerializer

redis_instance = redis.Redis(host=settings.REDIS_HOST,
                             port=settings.REDIS_PORT, db=0)


class ShortenURLAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ShortenedURLSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        shortened_url = serializer.save()

        redis_instance.set(name=shortened_url.short_url,
                           value=shortened_url.long_url)
        redis_instance.set(name=shortened_url.redis_counter_key,
                           value=0)

        return Response(data={'shortened_url': shortened_url.short_url},
                        status=status.HTTP_201_CREATED)


class RedirectAPIView(GenericAPIView):
    pass
