from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from catalog.models import Product
from .cart import Cart

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, is_available=True)
    quantity = int(request.POST.get('quantity', 1))
    
    cart.add(product=product, quantity=quantity, override_quantity=False)
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_total_items': len(cart),
            'cart_total_price': str(cart.get_total_price())
        })
    
    return redirect('cart:detail')

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_total_items': len(cart),
            'cart_total_price': str(cart.get_total_price())
        })
    
    return redirect('cart:detail')

@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    quantity = int(request.POST.get('quantity', 1))
    cart.update_quantity(product_id, quantity)
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        for item in cart:
            if str(item['product'].id) == str(product_id):
                return JsonResponse({
                    'success': True,
                    'item_total': str(item['total_price']),
                    'cart_total': str(cart.get_total_price()),
                    'cart_total_items': len(cart)
                })
    
    return redirect('cart:detail')