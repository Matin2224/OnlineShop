# Generated by Django 4.2 on 2024-08-20 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_alter_productorder_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Total Payment'),
        ),
        migrations.AlterField(
            model_name='productorder',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Total Price'),
        ),
    ]