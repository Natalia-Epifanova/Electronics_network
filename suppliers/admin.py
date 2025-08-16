from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.urls import reverse
from django.utils.html import format_html

from suppliers.models import Contact, Product, Supplier


@admin.register(Contact)
class ContactAdmin(ModelAdmin):
    """
    Административный интерфейс для модели Contact.

    Настройки:
        list_filter: Фильтры в правой панели (по всем полям модели)
    """

    list_filter = ("id", "email", "country", "city", "street", "house_number")


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    """
    Административный интерфейс для модели Product.

    Настройки:
        list_filter: Фильтры по ID, названию, модели и дате выхода
    """

    list_filter = (
        "id",
        "name",
        "model",
        "release_date",
    )


@admin.register(Supplier)
class SupplierAdmin(ModelAdmin):
    """
    Административный интерфейс для модели Supplier с расширенными функциями.

    Настройки:
        list_display: Отображаемые поля в списке
        list_filter: Фильтр по стране контакта
        actions: Пользовательские действия

    Методы:
        upstream_supplier_link: Ссылка на поставщика выше по цепочке
        clear_debt: Action для очистки задолженности

    Особенности:
        - Отображение уровня иерархии
        - Кликабельные ссылки на связанных поставщиков
        - Массовое управление задолженностью
    """

    list_display = ("name", "type", "debt", "upstream_supplier_link", "level")
    list_filter = ("contact__country",)
    actions = ["clear_debt"]

    def upstream_supplier_link(self, obj):
        """
        Создает HTML-ссылку на поставщика выше по цепочке.

        Args:
            obj: Экземпляр модели Supplier

        Returns:
            HTML-ссылка или None, если поставщика нет
        """
        if obj.upstream_supplier:
            return format_html(
                '<a href="{}">{}</a>',
                reverse(
                    "admin:suppliers_supplier_change", args=[obj.upstream_supplier.id]
                ),
                obj.upstream_supplier.name,
            )
        return None

    upstream_supplier_link.short_description = "Поставщик"

    def clear_debt(self, request, queryset):
        """
        Admin action для обнуления задолженности у выбранных поставщиков.

        Args:
            request: HttpRequest объект
            queryset: Выбранные объекты Supplier
        """
        queryset.update(debt=0)

    clear_debt.short_description = "Очистить долг у выбранных поставщиков"
