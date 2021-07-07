from django.conf import settings
from django.db import models
from django.core.cache import cache


class Brand(models.Model):
    name = models.CharField(max_length=64, unique=True)
    is_active = models.BooleanField(default=True, db_index=True)

    def __str__(self):
        return self.name


class Serial(models.Model):
    name = models.CharField(max_length=64, unique=True)
    is_active = models.BooleanField(default=True, db_index=True)

    def __str__(self):
        return self.name


class Sculptor(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class ProductProperties(models.Model):
    jan_code = models.IntegerField()
    size = models.CharField(max_length=32, null=True, blank=True)
    scale = models.CharField(max_length=8, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    serial = models.ForeignKey(Serial, on_delete=models.SET_NULL, null=True, blank=True)
    sculptor = models.ForeignKey(Sculptor, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.jan_code)


class Product(models.Model):
    name = models.CharField(max_length=64, unique=True)
    image = models.ImageField(upload_to='Product_images')
    price = models.DecimalField(max_digits=7, decimal_places=2)
    release = models.DateField()
    quantity = models.PositiveIntegerField(default=0)
    properties = models.OneToOneField(ProductProperties, on_delete=models.CASCADE, related_name='toProduct')
    is_active = models.BooleanField(default=True, db_index=True)

    def __str__(self):
        return self.name

    @staticmethod
    def get_items():
        return Product.objects.filter(is_active=True).order_by('name').select_related()


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.get_items()
            cache.set(key, products)
        return products
    else:
        return Product.get_items()
