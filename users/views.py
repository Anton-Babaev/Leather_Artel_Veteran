from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from .forms import UserRegistrationForm, UserLoginForm, ProfileUpdateForm
from .models import Wishlist
from catalog.models import Product
from orders.models import Order

def register(request):
    """
    Регистрация пользователя
    """
    if request.user.is_authenticated:
        return redirect('users:profile')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('users:profile')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    """
    Авторизация пользователя
    """
    if request.user.is_authenticated:
        return redirect('users:profile')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {user.username}!')
                
                # Перенаправление на следующую страницу или профиль
                next_url = request.GET.get('next', 'users:profile')
                return redirect(next_url)
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    else:
        form = UserLoginForm()
    
    return render(request, 'users/login.html', {'form': form})

def user_logout(request):
    """
    Выход пользователя
    """
    logout(request)
    messages.info(request, 'Вы вышли из аккаунта')
    return redirect('home')

@login_required
def profile(request):
    """
    Личный кабинет
    """
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            # Обновляем данные пользователя
            request.user.first_name = request.POST.get('first_name')
            request.user.last_name = request.POST.get('last_name')
            request.user.email = request.POST.get('email')
            request.user.save()
            
            # Сохраняем профиль
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('users:profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    
    # Получаем заказы пользователя
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    # Получаем избранное пользователя — ДОБАВЛЯЕМ ЭТУ СТРОКУ
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    
    context = {
        'form': form,
        'orders': orders,
        'wishlist_items': wishlist_items,  # ДОБАВЛЯЕМ ЭТУ СТРОКУ
    }
    return render(request, 'users/profile.html', context)

@login_required
def order_detail(request, order_id):
    """
    Детальная страница заказа
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'users/order_detail.html', {'order': order})

@login_required
def wishlist(request):
    """
    Избранное пользователя
    """
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'users/wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def wishlist_add(request, product_id):
    """
    Добавление товара в избранное
    """
    product = get_object_or_404(Product, id=product_id, is_available=True)
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'action': 'added' if created else 'removed',
            'message': 'Товар добавлен в избранное' if created else 'Товар удален из избранного'
        })
    
    return redirect('users:wishlist')

@login_required
def wishlist_remove(request, product_id):
    """
    Удаление товара из избранного
    """
    Wishlist.objects.filter(user=request.user, product_id=product_id).delete()
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Товар удален из избранного'})
    
    return redirect('users:wishlist')