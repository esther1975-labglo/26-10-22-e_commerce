# Generated by Django 4.1.2 on 2022-11-01 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_alter_brand_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitems',
            name='tax',
            field=models.IntegerField(default=2.25),
        ),
    ]
