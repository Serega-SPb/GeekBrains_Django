from django import forms

from ordersapp.models import *


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ()


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        exclude = ()
