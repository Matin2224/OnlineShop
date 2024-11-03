# Generated by Django 4.2 on 2024-08-07 13:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('website', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('customers', '0001_initial'),
        ('accounts', '0001_initial'),
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopproduct',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='website.product', verbose_name='Product'),
        ),
        migrations.AddField(
            model_name='shopproduct',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_products', to='dashboard.shop', verbose_name='Shop'),
        ),
        migrations.AddField(
            model_name='shop',
            name='address',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='shop_address', to='accounts.address', verbose_name='Address'),
        ),
        migrations.AddField(
            model_name='rating',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype', verbose_name='Content Type'),
        ),
        migrations.AddField(
            model_name='rating',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.customer', verbose_name='User'),
        ),
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together={('user', 'content_type', 'object_id')},
        ),
    ]
