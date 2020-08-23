from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('login', view=views.LoginAPIView.as_view(), name='login'),
    path('signup', view=views.SignUpAPIView.as_view(), name='signup'),
    path('logout', view=views.LogoutAPIView.as_view(), name='logout')
]
