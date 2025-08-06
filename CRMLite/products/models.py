from django.db import models
from companies.models import Storage

class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название товара')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество на складе')
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Закупочная цена')
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена продажи')
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, related_name='products', verbose_name='Склад')
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
    
    def __str__(self):
        return f"{self.title} (остаток: {self.quantity})"