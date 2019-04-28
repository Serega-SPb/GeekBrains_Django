import random
from django.shortcuts import render, get_object_or_404
from .models import *
# Create your views here.


def base():
    return {'menu_items': [
        {'name': 'Главная', 'link': 'index'},
        {'name': 'Каталог', 'link': 'catalog:index', 'namespace': 'catalog'},
        {'name': 'Контакты', 'link': 'contacts'},
        {'name': 'Admin', 'link': 'admin_custom:index'}
    ]}


def main(request):
    context = base()
    context['product'] = random.sample(list(Product.objects.all()), 1)[0]
    return render(request, 'mainapp/index.html', context=context)


def catalog(request, cat_id=None):
    context = base()
    context['cat_id'] = cat_id
    context['categories'] = Serial.objects.all()
    if cat_id and int(cat_id) > 0:
        cat = get_object_or_404(Serial, id=cat_id)
        props = ProductProperties.objects.filter(serial=cat).all()
        context['items'] = Product.objects.filter(properties__in=props).all()
    else:
        context['items'] = Product.objects.all()
        context['hot_items'] = random.sample(list(context['items']), 3)[:3]
    return render(request, 'mainapp/catalog.html', context=context)


def get_props(prop):
    return {
        'JAN': prop.jan_code,
        'Size': prop.size,
        'Scale': prop.scale,
        'Brand': prop.brand,
        'Serial': prop.serial,
        'Sculptor': prop.sculptor}


def gety_product_info(product):
    return {
        'id': product.id,
        'name': product.name,
        'image': product.image,
        'price': product.price,
        'release': product.release,
        'properties': list([(k, v) for k, v in get_props(product.properties).items() if k and v ])
    }


def product(request, id):
    context = base()
    product = Product.objects.filter(id=id).first()
    context.update(gety_product_info(product))

    return render(request, 'mainapp/product.html', context=context)


def contacts(request):
    context = base()
    return render(request, 'mainapp/contacts.html', context=context)

