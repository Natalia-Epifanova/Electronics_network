from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ModelViewSet

from suppliers.models import Contact, Product, Supplier
from suppliers.serializers import (
    ContactSerializer,
    ProductSerializer,
    SupplierSerializer,
)


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="Получение списка всех контактов."
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(operation_description="Создание нового контакта."),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_description="Просмотр детальной информации о контакте."
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(operation_description="Полное обновление контакта."),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        operation_description="Частичное обновление контакта."
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(operation_description="Удаление контакта."),
)
class ContactViewSet(ModelViewSet):
    """
    ViewSet для работы с контактами поставщиков.

    Предоставляет CRUD операции для контактной информации.
    """

    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="Получение списка всех продуктов."
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(operation_description="Создание нового продукта."),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_description="Просмотр детальной информации о продукте."
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        operation_description="Полное обновление информации о продукте."
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        operation_description="Частичное обновление информации о продукте."
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(operation_description="Удаление продукта."),
)
class ProductViewSet(ModelViewSet):
    """
    ViewSet для работы с продуктами.

    Предоставляет CRUD операции для продуктов электроники.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="Получение списка всех поставщиков."
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(operation_description="Создание нового поставщика."),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_description="Просмотр детальной информации о поставщике."
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        operation_description="Полное обновление информации о поставщике."
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        operation_description="Частичное обновление информации о поставщике."
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(operation_description="Удаление поставщика."),
)
class SupplierViewSet(ModelViewSet):
    """
    ViewSet для работы с поставщиками электроники.

    Иерархическая структура поставщиков:
    - Завод (уровень 0)
    - Розничная сеть (уровень 1)
    - Индивидуальный предприниматель (уровень 2)

    Особенности:
    - Поле 'debt' доступно только для чтения
    - Автоматический расчет уровня иерархии
    - Связь с контактами и продуктами

    Доступные фильтры:
    - ?contact__country=Россия - фильтр по стране
    - ?contact__city=Москва - фильтр по городу
    - ?type=1 - фильтр по типу поставщика
    """

    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        "contact__country": ["exact"],
        "contact__city": ["exact"],
        "type": ["exact"],
    }
