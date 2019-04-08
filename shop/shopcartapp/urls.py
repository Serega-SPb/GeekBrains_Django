from django.conf.urls import url
from . import views

app_name = 'shopcartapp'

urlpatterns = [
    url('^$', views.cart, name='cart'),
    url(r'add/(?P<pr_id>\d+)', views.cart_add, name='add'),
    url(r'remove/(?P<pr_id>\d+)', views.cart_remove, name='remove')
]
