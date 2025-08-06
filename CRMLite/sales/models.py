from django.db import models
from django.core.validators import MinValueValidator
from companies.models import Company
from products.models import Product

class Sale(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='sales', verbose_name='Компания')
    buyer_name = models.CharField(max_length=255, verbose_name='Имя покупателя')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата продажи')
    products = models.ManyToManyField(Product, through='ProductSale', related_name='sales', verbose_name='Товары')
    
    class Meta:
        verbose_name = 'Продажа'
        verbose_name_plural = 'Продажи'
    
    def __str__(self):
        return f"Продажа #{self.id} для {self.buyer_name}"


class ProductSale(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, verbose_name='Продажа')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='Товар')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name='Количество')
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена продажи')
    
    class Meta:
        verbose_name = 'Товар в продаже'
        verbose_name_plural = 'Товары в продажах'
        unique_together = ('sale', 'product')
    
    def __str__(self):
        return f"{self.product.title} в продаже {self.sale.id}"    
