from django.urls import path

from . import views

app_name = 'shortener'

url_patterns = [
    path('<slug:short_url>', view=views.RedirectAPIView.as_view(),
         name='short_url_redirection'),
    path('short-url', view=views.ShortenURLAPIView.as_view(),
         name='short_url')
]
