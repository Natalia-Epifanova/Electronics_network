from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from suppliers.models import Contact, Product, Supplier


class ContactSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class SupplierSerializer(ModelSerializer):
    contact = ContactSerializer()
    products = ProductSerializer(many=True)

    def validate(self, data):
        if data['upstream_supplier'] == self.instance:
            raise serializers.ValidationError("Поставщик не может ссылаться сам на себя")
        return data

    class Meta:
        model = Supplier
        fields = '__all__'
        read_only_fields = ('debt',)

