from .models import Category


def categories(request):
    """Передает категории во все шаблоны"""
    categories = Category.objects.filter(is_active=True, parent__isnull=True)
    return {
        'categories': categories
    }
