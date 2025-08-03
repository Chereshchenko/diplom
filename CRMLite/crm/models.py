from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MinValueValidator

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_company_owner', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Email')
    is_company_owner = models.BooleanField(default=False, verbose_name='Владелец компании')
    company = models.ForeignKey('Company', on_delete=models.SET_NULL, null=True, blank=True, related_name='employees', verbose_name='Компания')
    
    username = None 
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager() 
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return self.email


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
    
    def __str__(self):
        return f"{self.product.title} в поставке {self.supply.id}"


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