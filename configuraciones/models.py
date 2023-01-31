from django.db import models

# Create your models here.
class ValoresBase(models.Model):
    valor_cifra_base=models.DecimalField(max_digits=30, decimal_places=2)
    valor_adicional=models.DecimalField(max_digits=30, decimal_places=2,null=True, blank=True)
    base=models.IntegerField()
    porcentaje_mora=models.IntegerField()