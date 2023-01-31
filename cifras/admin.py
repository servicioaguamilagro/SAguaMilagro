from django.contrib import admin
from .models import Cifras
# Register your models here.
class AdminCifras(admin.ModelAdmin):
    list_display = ["__str__","id_usuario","mes","anio","cifra","id_valores","estado"]
    
    #hereda del objeto contacto
class Meta(object):
    model = Cifras

#registra en el entorno del administrador el modelo contacto
admin.site.register(Cifras,AdminCifras)

# Register your models here.
