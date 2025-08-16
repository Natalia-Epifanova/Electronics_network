from django.db import models

class Contact(models.Model):
    email = models.EmailField(verbose_name="Email")
    country = models.CharField(max_length=100, verbose_name="Страна")
    city = models.CharField(max_length=100, verbose_name="Город")
    street = models.CharField(max_length=100, blank=True, null=True, verbose_name="Улица")
    house_number = models.CharField(max_length=5, blank=True, null=True, verbose_name="Номер дома")

    def __str__(self):
        return f"{self.email} ({self.city}, {self.country})"

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название продукта")
    model = models.CharField(max_length=100, verbose_name="Модель")
    release_date = models.DateField(verbose_name="Дата выхода продукта на рынок")

    def __str__(self):
        return f"{self.name} ({self.model})."

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class Supplier(models.Model):
    FACTORY = 0
    RETAIL = 1
    ENTREPRENEUR = 2

    TYPE_CHOICES = [
        (FACTORY, 'Завод'),
        (RETAIL, 'Розничная сеть'),
        (ENTREPRENEUR, 'Индивидуальный предприниматель'),
    ]

    name = models.CharField(max_length=100, verbose_name="Название")
    type = models.IntegerField(choices=TYPE_CHOICES, verbose_name="Тип")
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE, verbose_name="Контакт")
    products = models.ManyToManyField(Product, verbose_name="Продукты")
    upstream_supplier = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Поставщик выше по цепочке")
    debt = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Долг перед поставщиком")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время создания")



    @property
    def level(self):
        if self.upstream_supplier is None:
            return 0
        return self.upstream_supplier.level + 1

    def __str__(self):
        return f"{self.name} ({self.get_type_display()}.)"

    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"