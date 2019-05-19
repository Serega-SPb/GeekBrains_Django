from django.conf import settings
from django.db import models

from mainapp.models import Product


class Order(models.Model):

    class Meta:
        ordering = ('-created',)

    FORMING = 'FM'
    SENT_TO_PROCEED = 'STP'
    PROCEEDED = 'PRD'
    PAID = 'PD'
    READY = 'RDY'
    CANCEL = 'CNC'

    ORDER_STATUS_CHOICES = (
        (FORMING, 'формируется'),
        (SENT_TO_PROCEED, 'отправлен в обработку'),
        (PAID, 'оплачен'),
        (PROCEEDED, 'обрабатывается'),
        (READY, 'готов к выдаче'),
        (CANCEL, 'отменен'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='обновлен', auto_now=True)
    status = models.CharField(verbose_name='статус',
                              max_length=3,
                              choices=ORDER_STATUS_CHOICES,
                              default=FORMING)
    is_active = models.BooleanField(verbose_name='активен', default=True)

    def __str__(self):
        return f'ID - {self.id} | user - {self.user}'

    def get_total_quantity(self):
        return sum(self.orderitems.all().values_list('quantity', flat=True))

    def get_product_type_quantity(self):
        return self.orderitems.count()

    def get_total_cost(self):
        items = self.orderitems.select_related('product')
        return sum([i.quantity * i.product.price for i in items])


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="orderitems")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def get_product_cost(self):
        return self.product.price * self.quantity

