# Generated by Django 4.1.3 on 2022-12-08 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0009_alter_cliente_medidor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='apellidos',
            field=models.CharField(blank=True, default='', max_length=30, null=True),
        ),
    ]
