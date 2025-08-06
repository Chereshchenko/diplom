from django.db import models
from companies.models import Company

class Supplier(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название поставщика')
    inn = models.CharField(max_length=12, verbose_name='ИНН поставщика')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='suppliers', verbose_name='Компания')
    
    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'
        unique_together = ('inn', 'company') 
    
    def __str__(self):
        return self.title

