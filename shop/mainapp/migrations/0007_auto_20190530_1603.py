# Generated by Django 2.1.7 on 2019-05-30 13:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_auto_20190523_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='properties',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='toProduct', to='mainapp.ProductProperties'),
        ),
    ]