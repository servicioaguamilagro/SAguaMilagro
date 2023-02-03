from django.test import TestCase
from .models import Cobros
from clientes.models import Cliente
import datetime
# Create your tests here.

class CobrosTestCase(TestCase):
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
       
    def test_setUp_creationcobros(self):
        date = datetime.date.today()
        cliente = Cliente.objects.get(id=1)
        self.cobros = Cobros.objects.create(
           id_usuario=cliente,
           registro=date,
           fechacifra='enero 2013',
           total=5.31
           )
        cobros = Cobros.objects.get(id=1)
        self.assertEqual(cobros.fechacifra, 'enero 2013')
