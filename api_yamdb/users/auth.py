from django.contrib.auth.backends import ModelBackend

from .exceptions import ConfirmationCodeIsIncorrect, UserNotFound
from .models import User


class Backend(ModelBackend):
    """Класс процедуры аутентификации."""
    def authenticate(
        self, request, username=None, password=None,
        confirmation_code=None, **kwargs
    ):
        """Производит аутентификацию."""
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
        try:
            user = User.objects.get_by_natural_key(username)
        except User.DoesNotExist:
            raise UserNotFound
        else:
            if (
                password
                and user.check_password(password)
                and self.user_can_authenticate(user)
            ):
                return user
            elif confirmation_code and not user.check_confirmation_code(
                confirmation_code
            ):
                raise ConfirmationCodeIsIncorrect
            if self.user_can_authenticate(user):
                return user

    def get_user(self, user_id):
        """Возвращает пользователя в случае аутентифткации."""
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None
