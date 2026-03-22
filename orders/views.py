from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from cart.cart import Cart
from .models import Order, OrderItem
from .forms import OrderCreateForm

def order_create(request):
    """
    Оформление заказа
    """
    cart = Cart(request)
    
    if len(cart) == 0:
        messages.warning(request, 'Ваша корзина пуста')
        return redirect('catalog:product_list')
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            
            # Если пользователь авторизован, связываем заказ с ним
            if request.user.is_authenticated:
                order.user = request.user
            
            # Сохраняем общую сумму
            order.total_price = cart.get_total_price()
            order.save()
            
            # Создаем товары в заказе
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            
            # Очищаем корзину
            cart.clear()
            
            # Отправляем email уведомление
            send_order_confirmation_email(order)
            
            # Сохраняем ID заказа в сессии для страницы подтверждения
            request.session['order_id'] = order.id
            
            # Перенаправляем на страницу успеха
            return redirect('orders:order_created')
    else:
        # Если пользователь авторизован, заполняем поля из профиля
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
            }
        form = OrderCreateForm(initial=initial_data)
    
    return render(request, 'orders/create.html', {
        'form': form,
        'cart': cart
    })

def order_created(request):
    """
    Страница успешного оформления заказа
    """
    order_id = request.session.get('order_id')
    if not order_id:
        return redirect('catalog:product_list')
    
    order = get_object_or_404(Order, id=order_id)
    
    # Удаляем ID заказа из сессии
    del request.session['order_id']
    
    return render(request, 'orders/created.html', {'order': order})

def send_order_confirmation_email(order):
    """
    Отправка email подтверждения заказа
    """
    subject = f'Подтверждение заказа #{order.id}'
    
    # Формируем список товаров
    items_list = ''
    for item in order.items.all():
        items_list += f'- {item.product.name}: {item.quantity} шт. x {item.price} ₽ = {item.get_cost()} ₽\n'
    
    message = f'''
    Здравствуйте, {order.first_name}!
    
    Ваш заказ #{order.id} успешно оформлен.
    
    Состав заказа:
    {items_list}
    
    Общая сумма: {order.total_price} ₽
    
    Способ доставки: {order.delivery_method}
    Способ оплаты: {order.payment_method}
    Адрес доставки: {order.address}, {order.city}
    
    Статус заказа: {order.get_status_display()}
    
    Спасибо за покупку!
    
    С уважением,
    Кожевенная артель «Ветеран»
    '''
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [order.email],
        fail_silently=False,
    )