from datetime import datetime
from django.core.management.base import BaseCommand
from mainapp.models import *
from django.contrib.auth.models import User
import json
import os

JSON_PATH = 'mainapp/json'
models = {
    'Brand': Brand,
    'Series Title': Serial,
    'Sculptor': Sculptor
}


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r') as infile:
        return json.load(infile)


def clear_db():
    Product.objects.all().delete()
    ProductProperties.objects.all().delete()
    Brand.objects.all().delete()
    Serial.objects.all().delete()
    Sculptor.objects.all().delete()


def get_prop(prop_name, props):

    if prop_name in props:
        p = models[prop_name].objects.filter(name=props.get(prop_name))
        if p.exists():
            result = p
        else:
            result = models[prop_name](name=props.get(prop_name).title())
            result.save()
        return result


class Command(BaseCommand):
    def handle(self, *args, **options):
        products = load_from_json('products')
        clear_db()

        all = Serial(id=0, name='All')
        all.save()
        for pr in products:
            props = pr['properties']

            properties = ProductProperties()
            properties.jan_code = props['JAN code']
            properties.scale = props.get('Scale')
            properties.size = props.get('Size')

            properties.brand = get_prop('Brand', props)
            properties.serial = get_prop('Series Title', props)
            properties.sculptor = get_prop('Sculptor', props)
            properties.save()

            product = Product(name=pr['name'],
                              image=pr['img'],
                              price=pr['price'],
                              release=datetime.strptime(pr['Release Date'], '%b-%Y').date(),
                              properties=properties)
            product.save()

        from authapp.models import ShopUser

        ShopUser.objects.create_superuser('root', '', 'qazxsw!2', age=50)
