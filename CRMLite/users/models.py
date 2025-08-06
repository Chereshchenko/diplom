from django.db import models
from django.contrib.auth.models import AbstractUser
from users.managers import UserManager

class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Email')
    is_company_owner = models.BooleanField(default=False, verbose_name='Владелец компании')
    company = models.ForeignKey('companies.Company', on_delete=models.SET_NULL, null=True, blank=True, related_name='employees', verbose_name='Компания')
    
    username = None 
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager() 
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return self.email
