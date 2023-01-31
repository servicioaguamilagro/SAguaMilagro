from django import forms
from .models import ValoresBase

class formulario_valor_base(forms.ModelForm):
    class Meta:
        model = ValoresBase
        fields=["valor_cifra_base","valor_adicional","base","porcentaje_mora"]
