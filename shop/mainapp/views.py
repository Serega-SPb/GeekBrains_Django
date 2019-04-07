from django.shortcuts import render
from .models import *
# Create your views here.


def base():
    return {'menu_items': [
        {'name': 'Главная', 'link': 'index'},
        {'name': 'Каталог', 'link': 'catalog:index', 'namespace': 'catalog'},
        {'name': 'Контакты', 'link': 'contacts'},
    ]}


def main(request):
    return render(request, 'mainapp/index.html', context=base())


def catalog(request, cat_id=None):

    context = base()
    context['cat_id'] = cat_id
    context['categories'] = Serial.objects.all()
    if cat_id and int(cat_id) > 0:
        cat = Serial.objects.filter(id=cat_id)[0]
        prop = ProductProperties.objects.filter(serial=cat)[0]
        context['items'] = [Product.objects.filter(properties=prop)[0]]
    else:
        context['items'] = Product.objects.all()
    return render(request, 'mainapp/catalog.html', context=context)


def get_props(prop):
    return {
        'JAN': prop.jan_code,
        'Size': prop.size,
        'Scale': prop.scale,
        'Brand': prop.brand,
        'Serial': prop.serial,
        'Sculptor': prop.sculptor}


def product(request, id):

    context = base()
    product = Product.objects.filter(id=id)[0]
    context['name'] = product.name
    context['image'] = product.image
    context['price'] = product.price
    context['release'] = product.release
    context['properties'] = list([(k, v) for k, v in get_props(product.properties).items() if k and v ])

    return render(request, 'mainapp/product.html', context=context)


def contacts(request):
    return render(request, 'mainapp/contacts.html', context=base())

