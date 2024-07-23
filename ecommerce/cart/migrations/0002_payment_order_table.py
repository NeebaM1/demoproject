# Generated by Django 5.0.6 on 2024-07-15 06:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
        ('shop', '0002_products'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('amount', models.CharField(max_length=100)),
                ('order_id', models.CharField(blank=True, max_length=100)),
                ('razorpay_payment_id', models.CharField(blank=True, max_length=100)),
                ('paid', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Order_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_of_items', models.IntegerField()),
                ('phone', models.CharField(max_length=12)),
                ('address', models.TextField()),
                ('pin', models.CharField(max_length=30)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('order_id', models.CharField(blank=True, max_length=100)),
                ('payment_status', models.CharField(default='pending', max_length=30)),
                ('delivery_status', models.CharField(default='pending', max_length=30)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.products')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
