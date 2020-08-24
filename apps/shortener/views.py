from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import ShortenedURLSerializer


class ShortenURLAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ShortenedURLSerializer

    def get(self, request):
        pass

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
