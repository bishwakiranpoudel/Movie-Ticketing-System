# Generated by Django 5.0.4 on 2024-04-22 10:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20240422_1617'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='discount_price',
        ),
        migrations.AddField(
            model_name='ticket',
            name='status',
            field=models.CharField(choices=[('booked', 'Booked'), ('not_booked', 'Not Booked')], default='not_booked', max_length=20),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.customer'),
        ),
    ]