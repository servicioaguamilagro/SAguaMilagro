# Generated by Django 4.1.3 on 2022-12-07 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cifras', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cifras',
            name='valor_adicional',
            field=models.DecimalField(blank=True, decimal_places=15, max_digits=30, null=True),
        ),
        migrations.AlterField(
            model_name='cifras',
            name='valor_cifra',
            field=models.DecimalField(decimal_places=15, max_digits=30),
        ),
    ]
