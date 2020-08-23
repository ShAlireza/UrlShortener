from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model


class EmailAuthenticationBackend(BaseBackend):
    """
    Custom Email Backend to perform authentication via email
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=username)
            if (user.check_password(password) and
                    self.user_can_authenticate(user)):
                return user
        except user_model.DoesNotExist:
            return None

    def user_can_authenticate(self, user):
        """
        Reject users with is_active=False. Custom user models that don't have
        that attribute are allowed.
        """
        is_active = getattr(user, 'is_active', None)
        return is_active or is_active is None

    def get_user(self, user_id):
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None
