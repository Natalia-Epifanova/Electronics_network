from django.urls import include, path
from rest_framework.routers import DefaultRouter

from suppliers.apps import SuppliersConfig
from suppliers.views import ContactViewSet, ProductViewSet, SupplierViewSet

app_name = SuppliersConfig.name
router = DefaultRouter()
router.register(r"contact", ContactViewSet)
router.register(r"product", ProductViewSet)
router.register(r"supplier", SupplierViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
