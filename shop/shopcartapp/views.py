from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from mainapp.models import Product
from .models import ShopCart


def base():
    return {'menu_items': [
        {'name': 'Главная', 'link': 'index'},
        {'name': 'Каталог', 'link': 'catalog:index', 'namespace': 'catalog'},
        {'name': 'Контакты', 'link': 'contacts'},
    ]}


def user_product_count(user):
    return {'products_count': ShopCart.objects.filter(user=user).count()}


def cart(request):
    context = base()
    if request.user and request.user.is_active:
        context.update(user_product_count(request.user))
    context['cart_items'] = ShopCart.objects.filter(user=request.user).all()
    return render(request, 'shopcartapp/cart.html', context=context)


def cart_add(request, pr_id):
    product = get_object_or_404(Product, id=pr_id)
    cart = ShopCart.objects.filter(user=request.user, product=product).first()
    if not cart:
        cart = ShopCart(user=request.user, product=product)
    cart.quantity += 1
    cart.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cart_remove(request, pr_id):
    product = get_object_or_404(Product, id=pr_id)
    cart = ShopCart.objects.filter(user=request.user, product=product).first()
    if cart:
        if cart.quantity <= 1:
            cart.delete()
        else:
            cart.quantity -= 1
            cart.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
