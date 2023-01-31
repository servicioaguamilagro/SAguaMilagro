from django import forms
from .models import Cobros

class formulario_cobros(forms.ModelForm):
    class Meta:
        model = Cobros
        fields=["id_usuario", "registro","fechacifra","total"]