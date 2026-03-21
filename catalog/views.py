from django.shortcuts import render, get_object_or_404
from .models import Category, Product


def product_list(request, category_slug=None):
    """Список товаров"""
    category = None
    categories = Category.objects.filter(is_active=True)
    products = Product.objects.filter(is_available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug, is_active=True)
        products = products.filter(category=category)

    context = {
        'category': category,
        'categories': categories,
        'products': products,
    }
    return render(request, 'catalog/product_list.html', context)


def product_detail(request, id, slug):
    """Детальная страница товара"""
    product = get_object_or_404(Product, id=id, slug=slug, is_available=True)
    context = {
        'product': product,
    }
    return render(request, 'catalog/product_detail.html', context)
