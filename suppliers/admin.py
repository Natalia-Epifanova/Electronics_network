from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.urls import reverse
from django.utils.html import format_html

from suppliers.models import Supplier, Contact, Product


@admin.register(Contact)
class ContactAdmin(ModelAdmin):
    list_filter = ("id", "email", "country", "city", "street", "house_number")

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_filter = ("id", "name", "model", "release_date",)

@admin.register(Supplier)
class SupplierAdmin(ModelAdmin):
    list_display = ('name', 'type', 'debt', 'upstream_supplier_link', 'level')
    list_filter = ('contact__country',)
    actions = ['clear_debt']

    def upstream_supplier_link(self, obj):
        if obj.upstream_supplier:
            return format_html('<a href="{}">{}</a>',
                reverse('admin:suppliers_supplier_change', args=[obj.upstream_supplier.id]),
                obj.upstream_supplier.name)
        return None
    upstream_supplier_link.short_description = 'Поставщик'

    def clear_debt(self, request, queryset):
        queryset.update(debt=0)
    clear_debt.short_description = "Очистить долг у выбранных поставщиков"
