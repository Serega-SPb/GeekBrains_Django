from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db import transaction
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete
from django.forms import inlineformset_factory

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from mainapp.models import Product, get_products
from shopcartapp.models import ShopCart
from .models import Order, OrderItem
from .forms import OrderItemForm


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()
    cart = request.user.Cart.all()
    if cart:
        cart.delete()
    return HttpResponseRedirect(reverse('ordersapp:orders_list'))


@receiver(pre_save, sender=OrderItem)
@receiver(pre_save, sender=ShopCart)
def product_quantity_update_save(sender, update_fields, instance, **kwargs):
    if update_fields is 'quantity' or 'product':
        if instance.pk:
            instance.product.quantity -= instance.quantity - sender.objects.get(id=instance.pk).quantity
        else:
            instance.product.quantity -= instance.quantity
        instance.product.save()


@receiver(pre_delete, sender=OrderItem)
@receiver(pre_delete, sender=ShopCart)
def product_quantity_update_delete(sender, instance, **kwargs):
    instance.product.quantity += instance.quantity
    instance.product.save()


class AUBaseView(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated


class OrderList(AUBaseView, ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderItemsCreate(AUBaseView, CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('orders:orders_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        order_formset = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            formset = order_formset(self.request.POST)
        else:
            cart_items = self.request.user.Cart.select_related('product')
            if len(cart_items):
                products = list(get_products().values('id', 'name'))
                order_formset = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=len(cart_items))
                formset = order_formset()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = cart_items[num].product
                    form.fields['product'].choices = [('', '------')] + [(p['id'], p['name']) for p in products]
                    form.initial['quantity'] = cart_items[num].quantity
                    form.initial['price'] = cart_items[num].product.price

            else:
                formset = order_formset()

        data['orderitems'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super().form_valid(form)


class OrderItemsUpdate(AUBaseView, UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('orders:orders_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        order_formset = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=0)

        if self.request.POST:
            data['orderitems'] = order_formset(self.request.POST, instance=self.object)
        else:
            queryset = self.object.orderitems.select_related()
            formset = order_formset(instance=self.object, queryset=queryset)
            products = list(get_products().values('id', 'name'))
            for form in formset.forms:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price
                    form.fields['product'].choices = [('', '------')] + [(p['id'], p['name']) for p in products]
            data['orderitems'] = formset

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super().form_valid(form)


class OrderDelete(AUBaseView, DeleteView):
    model = Order
    success_url = reverse_lazy('ordersapp:orders_list')

    def post(self, request, *args, **kwargs):
        answer = request.POST.get('answer')
        if not answer:
            return HttpResponseNotFound()

        subject = self.model.objects.filter(id=kwargs['pk']).first()

        if answer == 'удалить':
            subject.is_active = False
            subject.save()

        return HttpResponseRedirect(self.success_url)


class OrderRead(AUBaseView, DetailView):
    model = Order
