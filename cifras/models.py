from django.db import models
from clientes.models import Cliente
from .choices import pagado


class Cifras(models.Model):
    id_usuario=models.ForeignKey(Cliente, null=True, on_delete=models.CASCADE)
    mes=models.CharField(max_length=10)
    anio=models.CharField(max_length=4)
    cifra=models.IntegerField()
    id_valores=models.CharField(max_length=10)
    estado=models.CharField(max_length=1, choices=pagado, default='n')

    def __str__(self): 
        #apunta con 
        return  self.estado
    class Meta:
        db_table = 'cifra'
        verbose_name = 'Cifra'
        verbose_name_plural = 'cifras'
        ordering = ['id']
