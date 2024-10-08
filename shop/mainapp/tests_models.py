from datetime import datetime
from django.test import TestCase
from mainapp.models import *


class ProductsTestCase(TestCase):
    def setUp(self):
        serial = Serial.objects.create(name="Serial_1")
        self.props_1 = ProductProperties.objects.create(serial=serial, jan_code=1234567890123)
        self.product_1 = Product.objects.create(name="Product_1",
                                                properties=self.props_1,
                                                release=datetime.now(),
                                                price=1999.5,
                                                quantity=150)
        self.props_2 = ProductProperties.objects.create(serial=serial, jan_code=2234567890123)
        self.product_2 = Product.objects.create(name="Product_2",
                                                properties=self.props_2,
                                                release=datetime.now(),
                                                price=1999.5,
                                                quantity=150)
        self.props_3 = ProductProperties.objects.create(serial=serial, jan_code=3234567890123)
        self.product_3 = Product.objects.create(name="Product_3",
                                                properties=self.props_3,
                                                release=datetime.now(),
                                                price=1999.5,
                                                quantity=150)

    def test_product_get(self):
        product_1 = Product.objects.get(name="Product_1")
        product_2 = Product.objects.get(name="Product_2")
        self.assertEqual(product_1, self.product_1)
        self.assertEqual(product_2, self.product_2)

    def test_product_properties(self):
        product_1 = Product.objects.get(name="Product_1")
        product_3 = Product.objects.get(name="Product_3")
        prop_1 = product_1.properties
        prop_3 = product_3.properties
        self.assertEqual(prop_1, self.props_1)
        self.assertEqual(prop_3, self.props_3)


