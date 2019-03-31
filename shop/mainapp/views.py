from django.shortcuts import render
import json
import os
# Create your views here.
products = []
categories = []


def load_products():
    global products
    path = os.path.join(os.getcwd(), 'static/content/products.json')
    with open(path, 'r') as file:
        products = json.load(file)


def load_categories():
    global categories
    serials = [p['properties']['Series Title'] for p in products]
    categories = [{'id': i, 'link': f'catalog{i}', 'name': s} for i, s in enumerate(serials)]
    categories.append({'id': -1, 'link': 'catalog', 'name': 'All'})


def base():
    return {'menu_items': [
        {'name': 'Главная', 'link': 'index'},
        {'name': 'Каталог', 'link': 'catalog'},
        {'name': 'Контакты', 'link': 'contacts'},
    ]}


def main(request):
    return render(request, 'mainapp/index.html', context=base())


def get_catalog_items(id):

    if id:
        filter = [c['name'] for c in categories if c['id'] == int(id)]
        return [{'id': i['id'], 'name': i['name'], 'img': i['img']}
                for i in products if i['properties']['Series Title'] in filter]
    else:
        return [{'id': i['id'], 'name': i['name'], 'img': i['img']} for i in products]


def catalog(request):

    context = base()
    context['page_name'] = 'Каталог'

    if len(products) == 0:
        load_products()
        load_categories()
    id = request.path.replace('/catalog', '')
    context['items'] = get_catalog_items(id)

    context['categories'] = categories

    return render(request, 'mainapp/catalog.html', context=context)


def product(request):

    context = base()
    if len(products) == 0:
        load_products()
    id = request.path.replace('/product_', '')

    item = [i for i in products if i['id'] == int(id)][0]
    context.update(item)
    return render(request, 'mainapp/product.html', context=context)


def contacts(request):
    return render(request, 'mainapp/contacts.html', context=base())

