from django import forms
from .models import Notificaciones

class formulario_valor_base(forms.ModelForm):
    class Meta:
        model = Notificaciones
        fields=["id_usuario","fecha"]