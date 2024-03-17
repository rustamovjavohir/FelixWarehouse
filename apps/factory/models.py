from django.db import models
from utils.models import BaseModel


class Product(BaseModel):
    name = models.CharField(max_length=255,
                            verbose_name='Название')
    code = models.CharField(max_length=255,
                            verbose_name='Код')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class Material(BaseModel):
    name = models.CharField(max_length=255,
                            verbose_name='Название')

    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалы'

    def __str__(self):
        return self.name


class ProductMaterial(BaseModel):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                verbose_name='Продукт')
    material = models.ForeignKey(Material,
                                 on_delete=models.CASCADE,
                                 verbose_name='Материал')
    quantity = models.FloatField(verbose_name='Количество')

    class Meta:
        verbose_name = 'Материал продукта'
        verbose_name_plural = 'Материалы продуктов'

    def __str__(self):
        return f'{self.product} - {self.material}'


class Warehouse(BaseModel):
    material = models.ForeignKey(Material,
                                 on_delete=models.CASCADE,
                                 verbose_name='Материал')
    remainder = models.FloatField(default=0,
                                  verbose_name='Остаток')
    price = models.FloatField(null=True, blank=True,
                              verbose_name='Цена')

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

    def __str__(self):
        return self.material.name
