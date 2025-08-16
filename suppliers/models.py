from django.db import models


class Contact(models.Model):
    """
    Модель контактной информации для поставщиков.

    Атрибуты:
        email (EmailField): Электронная почта (обязательное)
        country (CharField): Страна (макс. 100 символов, обязательное)
        city (CharField): Город (макс. 100 символов, обязательное)
        street (CharField): Улица (макс. 100 символов, опциональное)
        house_number (CharField): Номер дома (макс. 5 символов, опциональное)

    Методы:
        __str__: Возвращает строковое представление в формате "email (город, страна)"

    Пример:
        Contact(email="contact@example.com", country="Россия", city="Москва")
    """

    email = models.EmailField(verbose_name="Email")
    country = models.CharField(max_length=100, verbose_name="Страна")
    city = models.CharField(max_length=100, verbose_name="Город")
    street = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Улица"
    )
    house_number = models.CharField(
        max_length=5, blank=True, null=True, verbose_name="Номер дома"
    )

    def __str__(self):
        """Строковое представление контакта в формате: email (город, страна)"""
        return f"{self.email} ({self.city}, {self.country})"

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"


class Product(models.Model):
    """
    Модель продукта электроники.

    Атрибуты:
        name (CharField): Название продукта (макс. 100 символов, обязательное)
        model (CharField): Модель продукта (макс. 100 символов, обязательное)
        release_date (DateField): Дата выхода на рынок (обязательное)

    Методы:
        __str__: Возвращает строку в формате "Название (Модель)"

    Пример:
        Product(name="Смартфон", model="X10 Pro", release_date="2023-01-15")
    """

    name = models.CharField(max_length=100, verbose_name="Название продукта")
    model = models.CharField(max_length=100, verbose_name="Модель")
    release_date = models.DateField(verbose_name="Дата выхода продукта на рынок")

    def __str__(self):
        """Строковое представление продукта: Название (Модель)"""
        return f"{self.name} ({self.model})."

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class Supplier(models.Model):
    """
    Модель поставщика электроники с иерархической структурой.

    Уровни иерархии:
        - FACTORY (0): Завод (верхний уровень)
        - RETAIL (1): Розничная сеть
        - ENTREPRENEUR (2): Индивидуальный предприниматель

    Атрибуты:
        name (CharField): Название поставщика (макс. 100 символов)
        type (IntegerField): Тип из TYPE_CHOICES (обязательное)
        contact (OneToOneField): Контактная информация (обязательное)
        products (ManyToManyField): Список продуктов
        upstream_supplier (ForeignKey): Ссылка на поставщика выше по цепочке
        debt (DecimalField): Задолженность (макс. 10 цифр, 2 знака после запятой)
        created_at (DateTimeField): Дата создания (автоматически)

    Свойства:
        level: Возвращает уровень в иерархии (0 для заводов)

    Методы:
        __str__: Возвращает строку в формате "Название (Тип)"

    Пример:
        Supplier(
            name="ТехноПром",
            type=Supplier.RETAIL,
            contact=contact_instance,
            upstream_supplier=factory_instance
        )
    """

    FACTORY = 0
    RETAIL = 1
    ENTREPRENEUR = 2

    TYPE_CHOICES = [
        (FACTORY, "Завод"),
        (RETAIL, "Розничная сеть"),
        (ENTREPRENEUR, "Индивидуальный предприниматель"),
    ]

    name = models.CharField(max_length=100, verbose_name="Название")
    type = models.IntegerField(choices=TYPE_CHOICES, verbose_name="Тип")
    contact = models.OneToOneField(
        Contact, on_delete=models.CASCADE, verbose_name="Контакт"
    )
    products = models.ManyToManyField(Product, verbose_name="Продукты")
    upstream_supplier = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Поставщик выше по цепочке",
    )
    debt = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Долг перед поставщиком",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата и время создания"
    )

    @property
    def level(self):
        """
        Вычисляет уровень поставщика в иерархии:
            - 0: Завод (нет upstream_supplier)
            - 1: Прямой поставщик от завода
            - 2: Поставщик второго уровня и т.д.
        """
        if self.upstream_supplier is None:
            return 0
        return self.upstream_supplier.level + 1

    def __str__(self):
        """Строковое представление: Название (Тип)"""
        return f"{self.name} ({self.get_type_display()}.)"

    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"
