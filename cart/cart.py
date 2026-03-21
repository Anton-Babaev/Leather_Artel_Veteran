from decimal import Decimal
from django.conf import settings
from catalog.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = {}
            self.session[settings.CART_SESSION_ID] = cart
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        
        if self.cart[product_id]['quantity'] > product.stock:
            self.cart[product_id]['quantity'] = product.stock
        
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        
        # Создаем список для итерации, не изменяя self.cart
        cart_items = []
        for product in products:
            item = self.cart[str(product.id)].copy()
            item['product'] = product
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            cart_items.append(item)
        
        return iter(cart_items)

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        total = Decimal('0')
        for item in self.cart.values():
            total += Decimal(item['price']) * item['quantity']
        return total

    def clear(self):
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True

    def update_quantity(self, product_id, quantity):
        product_id = str(product_id)
        if product_id in self.cart:
            try:
                product = Product.objects.get(id=int(product_id))
                if quantity > product.stock:
                    quantity = product.stock
                if quantity <= 0:
                    self.remove(product)
                else:
                    self.cart[product_id]['quantity'] = quantity
                    self.session.modified = True
            except Product.DoesNotExist:
                del self.cart[product_id]
                self.session.modified = True
                