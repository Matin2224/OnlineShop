# Generated by Django 4.2 on 2024-09-03 21:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopproduct',
            name='average_rating',
            field=models.DecimalField(decimal_places=1, default=1.0, max_digits=2, validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(5.0)], verbose_name='Average Rating'),
        ),
        migrations.AddField(
            model_name='shopproduct',
            name='rating_count',
            field=models.IntegerField(default=0, verbose_name='Rating Count'),
        ),
        migrations.AddField(
            model_name='shopproduct',
            name='sum_rating',
            field=models.IntegerField(default=0, verbose_name='Sum Rating'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='status',
            field=models.CharField(choices=[('Submitted', 'Submitted'), ('Rejected', 'Rejected'), ('Approved', 'Approved'), ('Pending', 'Pending')], default='Submitted', max_length=100, verbose_name='Status'),
        ),
    ]