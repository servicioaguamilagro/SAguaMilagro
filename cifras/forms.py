from django import forms
from .models import Cifras

class formulario_cifras(forms.ModelForm):
    class Meta:
        model = Cifras
        fields=["id","id_usuario", "mes","anio","cifra","id_valores","estado"]
