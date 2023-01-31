from django.contrib import admin
from .models import Cliente
# Register your models here.
class AdminCliente(admin.ModelAdmin):
    list_display = ["__str__","nombres","apellidos","detalle","medidor","cedula","email","direccion","celular","deuda", "ultima_cifra"]
    
    #hereda del objeto contacto
class Meta(object):
    model = Cliente

#registra en el entorno del administrador el modelo contacto
admin.site.register(Cliente,AdminCliente)