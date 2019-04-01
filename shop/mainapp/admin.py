from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Product)
admin.site.register(ProductProperties)
admin.site.register(Brand)
admin.site.register(Serial)
admin.site.register(Sculptor)

