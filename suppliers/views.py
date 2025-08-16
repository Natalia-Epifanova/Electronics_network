from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from suppliers.models import Supplier, Contact, Product
from suppliers.serializers import SupplierSerializer, ContactSerializer, ProductSerializer


class ContactViewSet(ModelViewSet):

    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

class ProductViewSet(ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class SupplierViewSet(ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'contact__country': ['exact'],
        'contact__city': ['exact'],
        'type': ['exact'],
    }