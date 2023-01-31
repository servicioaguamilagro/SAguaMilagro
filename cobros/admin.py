from django.contrib import admin
from .models import Cobros
# Register your models here.
class AdminCobros(admin.ModelAdmin):
    list_display = ["__str__","id_usuario","registro","fechacifra","total"]
    
    #hereda del objeto 
class Meta(object):
    model = Cobros

#registra en el entorno del administrador el modelo 
admin.site.register(Cobros,AdminCobros)
