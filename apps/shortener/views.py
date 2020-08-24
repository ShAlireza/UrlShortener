import redis

from django.shortcuts import redirect
from django.conf import settings

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from .models import ShortenedURL
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
        key = shortened_url.key

        # Set created keys in redis for future redirection requests
        redis_instance.set(name=key,
                           value=shortened_url.long_url)
        redis_instance.set(name=ShortenedURL.redis_counter_key(key),
                           value=0)

        return Response(data={'shortened_url': shortened_url.short_url},
                        status=status.HTTP_201_CREATED)


class RedirectAPIView(GenericAPIView):

    def get(self, request, key):
        url = redis_instance.get(name=key)
        if not url:
            raise NotFound()

        redis_instance.incr(name=key)

        return redirect(to=url)
