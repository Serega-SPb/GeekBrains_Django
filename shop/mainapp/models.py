from django.db import models

# Create your models here.


class Brand(models.Model):
    name = models.CharField(max_length=64, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Serial(models.Model):
    name = models.CharField(max_length=64, unique=True)
    is_active = models.BooleanField(default=True)

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
    properties = models.OneToOneField(ProductProperties, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name



