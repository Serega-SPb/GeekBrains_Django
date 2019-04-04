from django.conf.urls import url
from . import views

app_name = 'mainapp'

urlpatterns = [
    url(r'^$', views.catalog, name='index'),
    url(r'^(?P<cat_id>\d+)', views.catalog, name='filter'),
    url(r'^product_(?P<id>\d+)', views.product, name='product')
]
