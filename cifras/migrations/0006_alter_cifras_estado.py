# Generated by Django 4.1.3 on 2022-12-12 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cifras', '0005_alter_cifras_id_valores'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cifras',
            name='estado',
            field=models.CharField(choices=[('s', 'si'), ('n', 'no')], default='n', max_length=1),
        ),
    ]
