# Generated by Django 4.1.3 on 2022-11-30 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0008_cliente_celular'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='medidor',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
