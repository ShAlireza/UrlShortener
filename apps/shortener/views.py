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
    # permission_classes = (IsAuthenticated,)
    serializer_class = ShortenedURLSerializer

    def get(self, request):
        print(request.user_agent.browser)
        print(request.user_agent.is_pc)
        return Response(data={'data': request.META['HTTP_USER_AGENT']})

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        shortened_url = serializer.save()

        # Set created keys in redis for future redirection requests
        shortened_url.set_on_redis(redis_instance)

        return Response(data={'shortened_url': shortened_url.short_url},
                        status=status.HTTP_201_CREATED)


class RedirectAPIView(GenericAPIView):

    def get(self, request, key):
        from .tasks import update_shortened_url
        url = redis_instance.get(name=key)
        if not url:
            raise NotFound()

        platform = self.get_platform()
        browser = request.user_agent.browser.family
        session_key = request.session.session_key

        # Handle database updates with celery tasks
        update_shortened_url.delay([key, platform, browser, session_key])

        return redirect(to=url)

    def get_platform(self):
        from .models import PlatFormTypes

        if self.request.user_agent.is_mobile:
            return PlatFormTypes.MOBILE
        elif self.request.user_agent.is_tablet:
            return PlatFormTypes.TABLET
        else:
            return PlatFormTypes.DESKTOP
