from django import forms
from .models import Cliente

class formulario_cliente(forms.ModelForm):
    class Meta:
        model = Cliente
        fields=["nombres", "apellidos","detalle","medidor","cedula","email","direccion","celular","deuda","ultima_cifra"]
