from django.shortcuts import render
from .models import *
# Create your views here.


def base():
    return {'menu_items': [
        {'name': 'Главная', 'link': 'index'},
        {'name': 'Каталог', 'link': 'catalog'},
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


def product(request, id):

    context = base()

    product = Product.objects.filter(id=id)[0]
    context['name'] = product.name
    context['image'] = product.image
    context['price'] = product.price
    context['release'] = product.release
    temp = list(product.properties.__dict__.items())[2:-1]
    context['properties'] = list([(k, v) for k, v in temp if k != 'NULL' and v != 'NULL'])

    return render(request, 'mainapp/product.html', context=context)


def contacts(request):
    return render(request, 'mainapp/contacts.html', context=base())

