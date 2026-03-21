from .cart import Cart


def cart(request):
    """
    Контекстный процессор для передачи корзины во все шаблоны
    """
    cart_obj = Cart(request)
    print(f"Контекстный процессор: корзина содержит {cart_obj.cart}")  # Отладка
    return {'cart': cart_obj}
