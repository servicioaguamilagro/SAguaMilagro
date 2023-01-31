from django.contrib import admin
from .models import Notificaciones

# Register your models here.
class AdminNotificaciones(admin.ModelAdmin):
    list_display = ["__str__","id_usuario","fecha"]
    
    #hereda del objeto contacto
class Meta(object):
    model = Notificaciones

#registra en el entorno del administrador el modelo contacto
admin.site.register(Notificaciones,AdminNotificaciones)