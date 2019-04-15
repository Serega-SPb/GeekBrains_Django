from django.urls import path
from .views import *

app_name = 'admin_custom'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('activation', activation_objects, name='activation'),

    path('users/create', UsersCreateView.as_view(), name='create_user'),
    path('users', UsersReadView.as_view(), name='read_user'),
    path('users/update/<int:pk>', UsersUpdateView.as_view(), name='update_user'),
    path('users/delete/<int:pk>', UsersDeleteView.as_view(), name='delete_user'),

    path('products/create', ProductsCreateView.as_view(), name='create_product'),
    path('products', ProductsReadView.as_view(), name='read_product'),
    path('products/update/<int:pk>', ProductsUpdateView.as_view(), name='update_product'),
    path('products/delete/<int:pk>', ProductsDeleteView.as_view(), name='delete_product'),

    path('serials/create', SerialsCreateView.as_view(), name='create_serial'),
    path('serials', SerialsReadView.as_view(), name='read_serial'),
    path('serials/update/<int:pk>', SerialsUpdateView.as_view(), name='update_serial'),
    path('serials/delete/<int:pk>', SerialsDeleteView.as_view(), name='delete_serial'),

]
