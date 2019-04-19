from django.db import models
from django.conf import settings
from mainapp.models import Product


class ShopCart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Cart')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def get_all(self):
        return self.user.Cart.select_related('product').all()

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @property
    def total_quantity(self):
        _items = self.get_all()
        _total_quantity = sum(list(map(lambda x: x.quantity, _items)))
        return _total_quantity

    @property
    def total_cost(self):
        _items = self.get_all()
        _total_cost = sum(list(map(lambda x: x.product_cost, _items)))
        return _total_cost

    def __str__(self):
        return f'{self.product} - {self.quantity} ({self.user})'
