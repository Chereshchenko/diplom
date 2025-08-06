from django.db import models
from django.core.validators import MinValueValidator
from suppliers.models import Supplier
from products.models import Product

class Supply(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='supplies', verbose_name='Поставщик')
    delivery_date = models.DateField(verbose_name='Дата поставки')
    products = models.ManyToManyField(Product, through='SupplyProduct', related_name='supplies', verbose_name='Товары')
    
    class Meta:
        verbose_name = 'Поставка'
        verbose_name_plural = 'Поставки'
        ordering = ['-delivery_date']
    
    def __str__(self):
        return f"Поставка от {self.supplier.title} ({self.delivery_date})"


class SupplyProduct(models.Model):
    supply = models.ForeignKey(Supply, on_delete=models.CASCADE, verbose_name='Поставка')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name='Количество')
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена закупки')
    
    class Meta:
        verbose_name = 'Товар в поставке'
        verbose_name_plural = 'Товары в поставках'
        unique_together = ('supply', 'product')
    
    def save(self, *args, **kwargs):
        self.product.quantity += self.quantity
        self.product.save()
        super().save(*args, **kwargs)    
    
    def __str__(self):
        return f"{self.product.title} в поставке {self.supply.id}"

