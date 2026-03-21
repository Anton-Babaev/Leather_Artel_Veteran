from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import Category, Product


def product_list(request, category_slug=None):
    """Список товаров с фильтрацией, поиском и пагинацией"""
    category = None
    categories = Category.objects.filter(is_active=True)
    products = Product.objects.filter(is_available=True)

    # Фильтрация по категории
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug, is_active=True)
        products = products.filter(category=category)

    # Поиск
    query = request.GET.get('q', '')
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(short_description__icontains=query) |
            Q(material__icontains=query)
        )

    # Фильтр по цене
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # Фильтр по наличию
    in_stock = request.GET.get('in_stock', '')
    if in_stock:
        products = products.filter(stock__gt=0)

    # Фильтр по новинкам
    is_new = request.GET.get('is_new', '')
    if is_new:
        products = products.filter(is_new=True)

    # Фильтр по хитам
    is_bestseller = request.GET.get('is_bestseller', '')
    if is_bestseller:
        products = products.filter(is_bestseller=True)

    # Сортировка
    sort_by = request.GET.get('sort', '-created_at')
    valid_sorts = ['price', '-price', 'name', '-name', 'created_at', '-created_at']
    if sort_by in valid_sorts:
        products = products.order_by(sort_by)
    else:
        products = products.order_by('-created_at')

    # Пагинация (12 товаров на странице)
    paginator = Paginator(products, 12)
    page = request.GET.get('page', 1)

    try:
        products_page = paginator.page(page)
    except PageNotAnInteger:
        products_page = paginator.page(1)
    except EmptyPage:
        products_page = paginator.page(paginator.num_pages)

    context = {
        'category': category,
        'categories': categories,
        'products': products_page,
        'paginator': paginator,
        'query': query,
        'min_price': min_price,
        'max_price': max_price,
        'in_stock': in_stock,
        'is_new': is_new,
        'is_bestseller': is_bestseller,
        'sort_by': sort_by,
    }
    return render(request, 'catalog/product_list.html', context)


def product_detail(request, id, slug):
    """Детальная страница товара"""
    product = get_object_or_404(Product, id=id, slug=slug, is_available=True)
    context = {
        'product': product,
    }
    return render(request, 'catalog/product_detail.html', context)
