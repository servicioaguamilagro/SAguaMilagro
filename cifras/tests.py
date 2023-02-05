from django.test import TestCase
from .models import Cifras
from clientes.models import Cliente
# Create your tests here.

class CifrasTestCase(TestCase):
    def setUp(self):
       self.cliente = Cliente.objects.create(
           nombres='Alexis',
           apellidos='Sanmartin',
           medidor='00256',
           cedula='0705643740',
           email='test@gmail.com',
           direccion='milagro',
           celular='0986532569'
       )

    def test_setUp_ingresarcifras(self):
        cliente = Cliente.objects.get(id=1)
        self.cifras = Cifras.objects.create(
           id_usuario=cliente,
           mes='enero',
           anio='2013',
           cifra='25',
           id_valores=1
           )
        cifra = Cifras.objects.get(id=1)
        self.assertEqual(cifra.cifra, 25)
        
    def test_setUp_editValores(self):
        cliente = Cliente.objects.get(id=1)
        self.cifras = Cifras.objects.create(
           id_usuario=cliente,
           mes='enero',
           anio='2013',
           cifra='25',
           id_valores=1
       )
        cifr = Cifras.objects.get(id=1)
        cifr.anio='2014'
        cifr.save()
        c=Cifras.objects.get(id=1)
        self.assertEqual(c.anio, '2014')
