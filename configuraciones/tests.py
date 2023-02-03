from django.test import TestCase
# Create your tests here.
from django.contrib.auth.models import User
from .models import ValoresBase

class UserTestCase(TestCase):
    def setUp(self):
       self.user = User.objects.create_user(
           username='Secretaria349',
           password='12345',
           is_staff=False
       )
    def test_setUp_creation(self):
        self.assertEqual(self.user.is_active,True)
        self.assertEqual(self.user.is_staff,False)
        self.assertEqual(self.user.is_superuser,False)
       
class SuperTestCase(TestCase):
    def setUp(self):
        self.user =User.objects.create_superuser(
            username='Secretaria349',
            password='12345',
            is_staff=True
        )
    def test_setUp_creationSU(self):
        self.assertEqual(self.user.is_active,True)
        self.assertEqual(self.user.is_staff,True)
        self.assertEqual(self.user.is_superuser,True)
        
class ValoresTestCase(TestCase):
    def setUp(self):
       self.valores = ValoresBase.objects.create(
           valor_cifra_base=3.00,
           valor_adicional=0.25,
           base=25,
           porcentaje_mora=15
       )
       
    def test_setUp_creation(self):
        valores = ValoresBase.objects.get(id=1)
        self.assertEqual(valores.base, 25)

