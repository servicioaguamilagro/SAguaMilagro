from django.db import models
from .choices import deuda
# Create your models here.
class Cliente(models.Model):
    nombres=models.CharField(max_length=50)
    apellidos=models.CharField(max_length=30,null=True, blank=True)
    detalle=models.CharField(max_length=30,null=True, blank=True)
    medidor=models.CharField(max_length=10, unique=True)
    cedula=models.CharField(max_length=15)
    email=models.EmailField()
    direccion=models.CharField(max_length=50,null=True, blank=True)
    celular=models.CharField(max_length=10,null=True, blank=True)
    deuda=models.CharField(max_length=1, choices=deuda, default='n',null=True, blank=True)
    ultima_cifra=models.CharField(max_length=30,default='null',null=True, blank=True)

    def __str__(self): 
        #apunta con email
        return  self.medidor
    class Meta:
        db_table = 'cliente'
        verbose_name = 'Cliente'
        verbose_name_plural = 'clientes'
        ordering = ['apellidos']
        