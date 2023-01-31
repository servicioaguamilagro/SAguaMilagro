from django.db import models
from clientes.models import Cliente

# Create your models here.
class Notificaciones(models.Model):
    id_usuario=models.ForeignKey(Cliente, null=True, on_delete=models.CASCADE)
    fecha=models.CharField(max_length=30)
    