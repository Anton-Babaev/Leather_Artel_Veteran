from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'total_price', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    list_editable = ['status']
    inlines = [OrderItemInline]
    readonly_fields = ['total_price', 'created_at']
    fieldsets = (
        ('Клиент', {
            'fields': ('user', 'first_name', 'last_name', 'email', 'phone')
        }),
        ('Доставка', {
            'fields': ('address', 'city', 'postal_code', 'delivery_method')
        }),
        ('Оплата', {
            'fields': ('payment_method', 'total_price')
        }),
        ('Статус', {
            'fields': ('status', 'comment')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'price', 'quantity']
    list_filter = ['order']