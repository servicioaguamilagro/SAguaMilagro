# Generated by Django 4.1.3 on 2023-01-12 17:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clientes', '0019_alter_cliente_detalle'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notificaciones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(auto_now_add=True)),
                ('id_usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='clientes.cliente')),
            ],
        ),
    ]
