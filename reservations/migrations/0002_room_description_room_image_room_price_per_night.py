# Generated by Django 5.0.7 on 2024-08-29 11:01

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='room',
            name='image',
            field=models.ImageField(blank=True, upload_to='room_images/'),
        ),
        migrations.AddField(
            model_name='room',
            name='price_per_night',
            field=models.DecimalField(decimal_places=2, default=100.00, max_digits=8),
            preserve_default=False,
        ),
    ]
