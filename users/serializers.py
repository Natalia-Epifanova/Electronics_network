from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSerializer(ModelSerializer):
    """
    Сериализатор для модели User.

    Обеспечивает:
    - Безопасное хеширование паролей при создании
    - Контроль видимости полей (пароль только для записи)
    - Валидацию данных пользователя

    Поля:
        id (readonly): Уникальный идентификатор
        username: Логин пользователя
        password: Пароль (только для записи)
        email: Электронная почта
        is_active: Флаг активности аккаунта

    Методы:
        create: Хеширует пароль перед сохранением
    """

    class Meta:
        model = User
        fields = ("id", "username", "password", "email", "is_active")
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        """
        Создает нового пользователя с хешированным паролем.

        Args:
            validated_data: Валидированные данные пользователя

        Returns:
            User: Созданный экземпляр пользователя
        """
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)
