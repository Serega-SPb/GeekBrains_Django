from django.db import models
from django.conf import settings
from mainapp.models import Product


class ShopCart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f'{self.product} - {self.quantity} ({self.user})'
