# Generated by Django 4.1.2 on 2022-11-04 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='cart',
            name='updated_on',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='cartitems',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='cartitems',
            name='updated_on',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='order',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='updated_on',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='product',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='updated_on',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='productorder',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='productorder',
            name='updated_on',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='wishlist',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='wishlist',
            name='updated_on',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
