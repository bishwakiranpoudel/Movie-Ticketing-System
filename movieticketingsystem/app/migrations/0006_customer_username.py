# Generated by Django 5.0.4 on 2024-04-22 11:16

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20240422_1701'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='username',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
    ]
