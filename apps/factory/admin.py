from django.contrib import admin
from apps.factory.models import Product, Material, ProductMaterial, Warehouse


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code')
    search_fields = ('name', 'code')


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)


@admin.register(ProductMaterial)
class ProductMaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'material', 'quantity')
    search_fields = ('product', 'material', 'quantity')


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('id', 'material', 'remainder', 'price')
    search_fields = ('material', 'remainder', 'price')
