from django.test import TestCase
from django.test.client import Client
from mainapp.models import Product, Serial
from django.core.management import call_command


class TestMainappSmoke(TestCase):
    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        self.client = Client()

    def test_mainapp_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/contacts/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/catalog/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/catalog/0')
        self.assertEqual(response.status_code, 200)

        for serial in Serial.objects.all():
            response = self.client.get(f'/catalog/{serial.pk}/')
            self.assertEqual(response.status_code, 200)

        for product in Product.objects.all():
            response = self.client.get(f'/catalog/product_{product.pk}/')
            self.assertEqual(response.status_code, 200)

    def tearDown(self):
        call_command('sqlsequencereset', 'mainapp', 'authapp', 'ordersapp', 'shopcartapp')
