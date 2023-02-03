from django.test import TestCase
from .models import Cliente

class ClienteTestCase(TestCase):
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

    def test_setUp_creation(self):
        cliente = Cliente.objects.get(id=1)
        self.assertEqual(cliente.medidor, '00256')
        
    def test_setUp_edit(self):
        cliente = Cliente.objects.get(id=1)
        cliente.medidor='36523'
        cliente.save()
        c=Cliente.objects.get(id=1)
        self.assertEqual(cliente.medidor, '36523')
        
    def test_setUp_delete(self):
        cliente = Cliente.objects.get(id=1)
        cliente.delete()
        self.assertIsNot(cliente.nombres, 'Alexis')
        
   

