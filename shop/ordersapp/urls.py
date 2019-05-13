from django.conf.urls import url
from .views import *

app_name = 'ordersapp'

urlpatterns = [
    url(r'^$', OrderList.as_view(), name='orders_list'),
    url(r'^forming/complete/(?P<pk>\d+)/$', order_forming_complete, name='order_forming_complete'),
    url(r'^create/$', OrderItemsCreate.as_view(), name='order_create'),
    url(r'^read/(?P<pk>\d+)/$', OrderRead.as_view(), name='order_read'),
    url(r'^update/(?P<pk>\d+)/$', OrderItemsUpdate.as_view(), name='order_update'),
    url(r'^delete/(?P<pk>\d+)/$', OrderDelete.as_view(), name='order_delete'),
]
