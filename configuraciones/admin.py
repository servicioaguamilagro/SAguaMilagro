from django.contrib import admin
from .models import ValoresBase

# Register your models here.
class AdminValores(admin.ModelAdmin):
    list_display = ["valor_cifra_base","valor_adicional","base","porcentaje_mora"]
    
    #hereda del objeto contacto
class Meta(object):
    model = ValoresBase

#registra en el entorno del administrador el modelo contacto
admin.site.register(ValoresBase,AdminValores)