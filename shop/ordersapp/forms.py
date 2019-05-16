from django import forms
from .models import *


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        exclude = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
