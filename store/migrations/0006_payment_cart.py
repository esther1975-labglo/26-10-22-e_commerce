# Generated by Django 4.1.2 on 2022-11-09 06:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_alter_payment_transaction_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='cart',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='store.cart'),
            preserve_default=False,
        ),
    ]
