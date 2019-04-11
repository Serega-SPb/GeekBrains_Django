from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse

from mainapp.models import Product
from .models import ShopCart


def base():
    return {'menu_items': [
        {'name': 'Главная', 'link': 'index'},
        {'name': 'Каталог', 'link': 'catalog:index', 'namespace': 'catalog'},
        {'name': 'Контакты', 'link': 'contacts'},
    ]}


def update_header(request):
    result = render_to_string('mainapp/includes/header.html', base(), request)
    return JsonResponse({'result': result})


@login_required
def cart(request):
    context = base()
    context['cart_items'] = ShopCart.objects.filter(user=request.user).all()
    return render(request, 'shopcartapp/cart.html', context=context)


@login_required
def cart_add(request, pr_id):
    product = get_object_or_404(Product, id=pr_id)
    cart = ShopCart.objects.filter(user=request.user, product=product).first()
    if not cart:
        cart = ShopCart(user=request.user, product=product)
    cart.quantity += 1
    cart.save()
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('catalog:index'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def cart_remove(request, pr_id):
    product = get_object_or_404(Product, id=pr_id)
    cart = ShopCart.objects.filter(user=request.user, product=product).first()
    if cart:
        cart.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def cart_edit(request):

    pr_id = int(request.GET.get('pr_id'))
    count = int(request.GET.get('count'))
    if pr_id <= 0 or count < 0:
        return HttpResponseNotFound()
    product = get_object_or_404(Product, id=pr_id)
    cart = ShopCart.objects.filter(user=request.user, product=product).first()
    if cart:
        if count > 0:
            cart.quantity = count
            cart.save()
        else:
            cart.delete()
            return HttpResponse('Changed')
    return HttpResponse('OK')
