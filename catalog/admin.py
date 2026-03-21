from django.contrib import admin
from .models import Category, Product, ProductImage


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent', 'is_active', 'order']
    list_filter = ['is_active', 'parent']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order', 'is_active']
    list_per_page = 20


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    fields = ['image', 'title', 'order', 'is_main']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'old_price', 'stock', 'is_available', 'is_new', 'is_bestseller']
    list_filter = ['category', 'is_available', 'is_new', 'is_bestseller', 'created_at']
    search_fields = ['name', 'description', 'material']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['price', 'stock', 'is_available', 'is_new', 'is_bestseller']
    list_per_page = 20
    inlines = [ProductImageInline]
    fieldsets = (
        ('Основная информация', {
            'fields': ('category', 'name', 'slug', 'description', 'short_description')
        }),
        ('Цены', {
            'fields': ('price', 'old_price')
        }),
        ('Изображения', {
            'fields': ('image',)
        }),
        ('Характеристики', {
            'fields': ('material', 'dimensions', 'weight', 'color')
        }),
        ('Статусы', {
            'fields': ('is_available', 'is_new', 'is_bestseller', 'is_featured', 'stock')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)