# Generated by Django 5.0.6 on 2024-06-23 13:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_paid', models.BooleanField(default=False, verbose_name='Оплачен')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(blank=True, db_index=True, max_length=36, null=True, verbose_name='Provider transaction ID')),
                ('status', models.CharField(choices=[('CREATED', 'Создана'), ('CANCELED', 'Отменена'), ('PAID', 'Оплачена')], default='CREATED', verbose_name='Статус')),
                ('payment_service', models.CharField(blank=True, choices=[('payme', 'Payme'), ('click', 'Click'), ('apelsin', 'Apelsin'), ('paynet', 'Paynet'), ('octo', 'Octo'), ('payze', 'Payze'), ('uzum', 'Uzum'), ('alif', 'Alif')], max_length=10, null=True, verbose_name='Платежная служба')),
                ('currency', models.CharField(choices=[('UZS', 'UZS'), ('USD', 'USD')], default='UZS', max_length=12, verbose_name='Валюта')),
                ('amount', models.PositiveIntegerField(verbose_name='Сумма')),
                ('additional_parameters', models.JSONField(blank=True, default=dict, null=True, verbose_name='Дополнительные параметры')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='transactions', to='payment.order', verbose_name='Заказ')),
            ],
            options={
                'verbose_name': 'Транзакция',
                'verbose_name_plural': 'Транзакции',
            },
        ),
    ]