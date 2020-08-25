from django.urls import path

from . import views

app_name = 'shortener'

urlpatterns = [
    path('short-url', view=views.ShortenURLAPIView.as_view(),
         name='short_url'),
    path('<slug:key>', view=views.RedirectAPIView.as_view(),
         name='short_url_redirection'),
]
