from django.contrib import admin
from django.contrib.admin import ModelAdmin

from users.models import User


@admin.register(User)
class UserAdmin(ModelAdmin):
    """
    Административный интерфейс для модели User.

    Настройки:
        list_filter: Фильтры по ID, имени и email
    """

    list_filter = ("id", "username", "email")
