# Generated by Django 5.0.7 on 2024-08-26 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_customuser_managers_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='stripe_payment_id',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='id транзакции'),
        ),
        migrations.AddField(
            model_name='payment',
            name='stripe_status',
            field=models.CharField(max_length=20, null=True, verbose_name='статус транзакции'),
        ),
    ]
