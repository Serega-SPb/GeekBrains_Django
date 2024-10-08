from django import forms

from mainapp.models import *
from ordersapp.models import *


class SerialForm(forms.ModelForm):

    discount = forms.IntegerField(label='Discount', required=False, min_value=0, max_value=100, initial=0)

    class Meta:
        model = Serial
        exclude = ()


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ()


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        exclude = ()
