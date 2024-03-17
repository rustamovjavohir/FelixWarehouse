from rest_framework import serializers
from apps.factory.models import Product, ProductMaterial, Warehouse, Material


class ProductSerializer(serializers.Serializer):
    product_qty = serializers.IntegerField(required=True)
    id = serializers.IntegerField(required=True)

    class Meta:
        fields = (
            'id',
            'product_qty',
        )
        read_only_fields = (
            'id',
            # 'product_qty'
        )


class FactorySerializer(serializers.Serializer):
    product = ProductSerializer(many=True)

    class Meta:
        fields = (
            'product',
        )


class ProductMaterialSerializer(serializers.ModelSerializer):
    material_name = serializers.CharField(source='material.name', read_only=True)
    qty = serializers.FloatField(source='quantity', read_only=True)

    class Meta:
        model = Warehouse
        fields = (
            'id',
            'product',
            'price',
            'qty'
        )
        read_only_fields = (
            'id',
        )
