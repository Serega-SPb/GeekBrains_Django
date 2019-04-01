from django.db import models

# Create your models here.


class Brand(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='Name')

    def __set__(self):
        return self.name


class Serial(models.Model):
    title = models.CharField(max_length=64, unique=True, verbose_name='Title')

    def __set__(self):
        return self.title


class Sculptor(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='Name')

    def __set__(self):
        return self.name


class ProductProperties(models.Model):
    jan_code = models.IntegerField()
    size = models.CharField(max_length=32, null=True, blank=True)
    scale = models.CharField(max_length=8, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    serial = models.ForeignKey(Serial, on_delete=models.SET_NULL, null=True, blank=True)
    sculptor = models.ForeignKey(Sculptor, on_delete=models.SET_NULL, null=True, blank=True)

    def __set__(self):
        return self.jan_code


class Product(models.Model):
    name = models.CharField(max_length=64, unique=True)
    image = models.ImageField(upload_to='Product_images')
    price = models.DecimalField(max_digits=7, decimal_places=2)
    release = models.DateField()
    properties = models.ForeignKey(ProductProperties, on_delete=models.SET_NULL, null=True, blank=True)

    def __set__(self):
        return self.name



