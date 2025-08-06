from django.db import models
from users.models import User

class Company(models.Model):
    title = models.CharField(max_length=255, unique=True, verbose_name='Название компании')
    inn = models.CharField(max_length=20, unique=True, verbose_name='ИНН')
    owner = models.OneToOneField(User, on_delete=models.PROTECT, related_name='owned_company', verbose_name='Владелец')
    
    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'
    
    def __str__(self):
        return self.title


class Storage(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='storage', verbose_name='Компания')
    address = models.CharField(max_length=255, verbose_name='Адрес склада')
    
    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'
    
    def __str__(self):
        return f"Склад компании {self.company.title}"


