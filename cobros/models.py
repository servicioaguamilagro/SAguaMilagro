from django.db import models
from clientes.models import Cliente

# Create your models here.
class Cobros(models.Model):
    id_usuario=models.ForeignKey(Cliente, null=True, on_delete=models.CASCADE)
    registro=models.DateField()
    fechacifra=models.CharField(max_length=15)
    total=models.DecimalField(max_digits=30, decimal_places=2)

    def __str__(self): 
        #apunta con 
        return  self.id_usuario