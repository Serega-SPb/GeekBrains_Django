from django import template

register = template.Library()


@register.filter
def shopcart_status(user):
    if not user.is_authenticated:
        return None
    items = user.Cart.select_related('product')
    if not items:
        return None
    total = [sum(x) for x in zip(*[(x.quantity, x.product_cost) for x in items])]
    return {
        'quantity': total[0],
        'product_cost': total[1]
    }
