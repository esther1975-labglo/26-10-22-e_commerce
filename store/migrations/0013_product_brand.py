# Generated by Django 4.1.2 on 2022-11-03 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_cart_created_on_cart_updated_on_cartitems_created_on_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.ImageField(default=2, upload_to='static/image/'),
            preserve_default=False,
        ),
    ]