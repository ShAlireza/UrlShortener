from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import APIException
from rest_framework import status


class PasswordsNotMatch(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Passwords entered don\'t match')
    default_code = 'passwords_not_match'
