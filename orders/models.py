from django.db import models
from django.contrib.auth.models import User
from catalog.models import Product

class Order(models.Model):
    """
    Модель заказа
    """
    STATUS_CHOICES = (
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('paid', 'Оплачен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),
    )
    
    # Данные пользователя
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Пользователь',
        related_name='orders'
    )
    
    # Контактные данные
    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    email = models.EmailField('Email')
    phone = models.CharField('Телефон', max_length=20)
    
    # Адрес доставки
    address = models.TextField('Адрес доставки')
    city = models.CharField('Город', max_length=100)
    postal_code = models.CharField('Индекс', max_length=20, blank=True)
    
    # Информация о заказе
    comment = models.TextField('Комментарий к заказу', blank=True)
    total_price = models.DecimalField('Общая сумма', max_digits=10, decimal_places=2)
    
    # Статусы
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='new')
    
    # Способы доставки и оплаты
    delivery_method = models.CharField('Способ доставки', max_length=100, default='Самовывоз')
    payment_method = models.CharField('Способ оплаты', max_length=100, default='Наличными при получении')
    
    # Даты
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Заказ #{self.id} - {self.first_name} {self.last_name}'
    
    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    """
    Модель товара в заказе
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name='Заказ',
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Товар',
        related_name='order_items'
    )
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField('Количество', default=1)
    
    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'
    
    def __str__(self):
        return f'{self.product.name} x {self.quantity}'
    
    def get_cost(self):
        return self.price * self.quantity