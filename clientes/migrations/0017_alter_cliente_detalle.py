# Generated by Django 4.1.3 on 2022-12-12 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0016_alter_cliente_detalle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='detalle',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
