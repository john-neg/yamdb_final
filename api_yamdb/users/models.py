from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models


class User(AbstractUser):
    """Модель пользователя User."""
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"

    ROLE_CHOICES = [
        (USER, "Пользователь"),
        (MODERATOR, "Модератор"),
        (ADMIN, "Администратор"),
    ]

    email = models.EmailField(unique=True)
    bio = models.TextField(
        "Биография",
        blank=True,
    )
    role = models.CharField(
        "Роль",
        default=USER,
        max_length=16,
        choices=ROLE_CHOICES,
    )
    email_confirmed = models.BooleanField(
        "Email подтвержден",
        default=False,
    )
    confirmation_code = models.CharField(
        "Код подтверждения",
        blank=True,
        max_length=10,
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("username",)

    def send_confirmation_code(self):
        """Отправить код подтверждения."""
        if self.email and self.confirmation_code:
            send_mail(
                subject="API YamDb confirmation code",
                message=f"confirmation_code: {self.confirmation_code}",
                from_email=None,
                recipient_list=[self.email],
                fail_silently=True,
            )

    def check_confirmation_code(self, confirmation_code):
        """Проверить код подтверждения."""
        return (
            False
            if not confirmation_code or not isinstance(confirmation_code, str)
            else self.confirmation_code == confirmation_code
        )

    @property
    def is_admin(self):
        """Проверяет является ли пользователь администратором."""
        return self.role == User.ADMIN

    @property
    def is_moderator(self):
        """Проверяет является ли пользователь модератором."""
        return self.role == User.MODERATOR
