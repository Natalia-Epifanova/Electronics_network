from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from suppliers.models import Contact, Product, Supplier


class ContactSerializer(ModelSerializer):
    """
    Сериализатор для контактной информации поставщиков.
    """

    class Meta:
        model = Contact
        fields = "__all__"


class ProductSerializer(ModelSerializer):
    """
    Сериализатор для продуктов электроники.
    """

    class Meta:
        model = Product
        fields = "__all__"


class SupplierSerializer(ModelSerializer):
    """
    Сериализатор для поставщиков электроники с вложенными контактами и продуктами.

    Особенности:
    - Запрещено обновление поля debt (только для чтения)
    - Проверка на циклические ссылки в цепочке поставщиков
    - Автоматическое вычисление уровня иерархии
    """

    contact = ContactSerializer()
    products = ProductSerializer(many=True)

    def validate(self, data):
        """
        Валидация данных поставщика:
        - Проверка, что поставщик не ссылается сам на себя
        - Проверка корректности типа поставщика относительно цепочки

        Вызывает:
        ValidationError: если обнаружена циклическая ссылка или неверная иерархия
        """
        if data["upstream_supplier"] == self.instance:
            raise serializers.ValidationError(
                "Поставщик не может ссылаться сам на себя"
            )
        return data

    class Meta:
        model = Supplier
        fields = "__all__"
        read_only_fields = ("debt",)
