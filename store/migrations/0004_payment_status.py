# Generated by Django 4.1.2 on 2022-11-08 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='status',
            field=models.BooleanField(default=1),
        ),
    ]