from django.db import models
from django.urls import reverse

class Category(models.Model):
    """Модель категории товаров"""
    name = models.CharField('Название', max_length=200)
    slug = models.SlugField('URL', max_length=200, unique=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Родительская категория',
        related_name='children'
    )
    description = models.TextField('Описание', blank=True)
    image = models.ImageField('Изображение', upload_to='categories/', blank=True, null=True)
    is_active = models.BooleanField('Активна', default=True)
    order = models.PositiveIntegerField('Порядок сортировки', default=0)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('catalog:product_list_by_category', args=[self.slug])


class Product(models.Model):
    """Модель товара"""
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория',
        related_name='products'
    )
    name = models.CharField('Название', max_length=250)
    slug = models.SlugField('URL', max_length=250, unique=True)
    description = models.TextField('Описание')
    short_description = models.TextField('Краткое описание', max_length=500, blank=True)
    
    # Цены
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    old_price = models.DecimalField('Старая цена', max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Изображения
    image = models.ImageField('Главное изображение', upload_to='products/')
    
    # Характеристики
    material = models.CharField('Материал', max_length=100, blank=True)
    dimensions = models.CharField('Размеры', max_length=100, blank=True)
    weight = models.CharField('Вес', max_length=50, blank=True)
    color = models.CharField('Цвет', max_length=50, blank=True)
    
    # Статусы
    is_available = models.BooleanField('В наличии', default=True)
    is_new = models.BooleanField('Новинка', default=False)
    is_bestseller = models.BooleanField('Хит продаж', default=False)
    is_featured = models.BooleanField('Рекомендуемый', default=False)
    
    # Количество
    stock = models.PositiveIntegerField('Количество на складе', default=0)
    
    # SEO
    meta_title = models.CharField('Meta Title', max_length=250, blank=True)
    meta_description = models.TextField('Meta Description', max_length=500, blank=True)
    meta_keywords = models.CharField('Meta Keywords', max_length=250, blank=True)
    
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('catalog:product_detail', args=[self.id, self.slug])
    
    def get_price_with_discount(self):
        """Возвращает цену со скидкой"""
        return self.old_price if self.old_price else self.price


class ProductImage(models.Model):
    """Дополнительные изображения товара"""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар',
        related_name='images'
    )
    image = models.ImageField('Изображение', upload_to='products/gallery/')
    title = models.CharField('Название', max_length=100, blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)
    is_main = models.BooleanField('Основное', default=False)
    
    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товаров'
        ordering = ['order']
    
    def __str__(self):
        return f"{self.product.name} - {self.order}"