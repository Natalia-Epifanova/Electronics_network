from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Кастомная модель пользователя, расширяющая стандартную AbstractUser.

    Добавляет возможность управления активностью пользователей через поле is_active.

    Атрибуты:
        is_active (BooleanField): Флаг активности пользователя (по умолчанию True)

    Наследует все поля от AbstractUser:
        username, password, email, first_name, last_name и др.

    Пример использования:
        user = User.objects.create_user(username='test', password='123', is_active=True)
    """

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
