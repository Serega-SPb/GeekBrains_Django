import random

from django.http import JsonResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

from .models import *


def get_product_price(request):
    id = request.GET.get('id')
    price = Product.objects.get(id=id).price
    result = {
        'id': id,
        'price': price
    }
    return JsonResponse(result)


def main(request):
    context = {
        'product': random.sample(list(get_products()), 1)[0]
    }
    return render(request, 'mainapp/index.html', context=context)


def catalog(request, cat_id=None):
    context = {
        'cat_id': cat_id,
        'categories': Serial.objects.all(),
    }
    if cat_id and int(cat_id) > 0:
        cat = get_object_or_404(Serial, id=cat_id)
        props = ProductProperties.objects.filter(serial=cat).all()
        context['items'] = get_products().filter(properties__in=props).all()
    else:
        context['items'] = get_products()
        context['hot_items'] = random.sample(list(context['items']), 3)[:3]
    return render(request, 'mainapp/catalog.html', context=context)


def catalog_ajax(request):
    cat_id = int(request.GET.get('cat_id'))
    if cat_id and int(cat_id) > 0:
        cat = get_object_or_404(Serial, id=cat_id)
        context = {'items': get_products().filter(properties__in=ProductProperties.objects.filter(serial=cat))}
    else:
        context = {'items': get_products()}
    result = render_to_string('mainapp/includes/catalog_content.html', request=request, context=context)
    return JsonResponse({'result': result})


def get_props(prop):
    return {
        'JAN': prop.jan_code,
        'Size': prop.size,
        'Scale': prop.scale,
        'Brand': prop.brand,
        'Serial': prop.serial,
        'Sculptor': prop.sculptor}


def get_product_info(product):
    return {
        'id': product.id,
        'name': product.name,
        'image': product.image,
        'price': product.price,
        'release': product.release,
        'properties': list([(k, v) for k, v in get_props(product.properties).items() if k and v ])
    }


def product(request, id):
    _product = get_products().filter(id=id).first()
    context = get_product_info(_product)
    return render(request, 'mainapp/product.html', context=context)


def contacts(request):
    return render(request, 'mainapp/contacts.html')

