import json
import sqlite3
from datetime import datetime

connection = None


def write_into_db(table, data):

    temp = []
    for d in data:
        temp.append(', '.join([f'"{v}"' for v in d.values()]))
    values = ', '.join([f'("{i}",{v})' for i, v in enumerate(temp, 1)])
    command = f'INSERT INTO {table} VALUES {values}'
    connection.execute(command)


def parse_data(data):
    products = []
    properties = []
    brands = []
    sculptors = []
    serials = []

    for d in data:

        ps = d['properties']
        brand = ps.get('Brand')
        serial = ps.get('Series Title')
        sculptor = ps.get('Sculptor')

        props = {'jan': ps['JAN code']}
        if 'Size' in ps:
            props['size'] = ps['Size']
        else:
            props['size'] = 'NULL'
        if 'Scale' in ps:
            props['scale'] = ps['Scale']
        else:
            props['scale'] = 'NULL'

        if brand:
            brands.append({'name': brand})
            props['brand_id'] = len(brands)
        else:
            props['brand_id'] = 'NULL'

        if serial:
            serials.append({'name': serial})
            props['serial_id'] = len(serials)
        else:
            props['serial_id'] = 'NULL'
        if sculptor:
            sculptors.append({'name': sculptor})
            props['sculptor_id'] = len(sculptors)
        else:
            props['sculptor_id'] = 'NULL'

        properties.append(props)
        products.append({
            'name': d['name'],
            'image': d['img'],
            'price': d['price'],
            'release': datetime.strptime(d['Release Date'], '%b-%Y').date(),
            'properties_id': len(properties)
        })

    write_into_db('mainapp_brand', brands)
    write_into_db('mainapp_serial', serials)
    write_into_db('mainapp_sculptor', sculptors)
    write_into_db('mainapp_productproperties', properties)
    write_into_db('mainapp_product', products)


def load(json_file):
    global connection
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    connection = sqlite3.connect('db.sqlite3')
    parse_data(data)
    connection.commit()
    connection.close()


if __name__ == '__main__':
    load('static/content/products.json')
