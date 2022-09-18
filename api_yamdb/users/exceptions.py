from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_404_NOT_FOUND


class ConfirmationCodeIsIncorrect(Exception):
    """Некорректный код подтверждения."""
    pass


class UserNotFound(APIException):
    """Пользователь не найден."""
    status_code = HTTP_404_NOT_FOUND
    default_detail = _('Incorrect username.')
    default_code = 'username_failed'
