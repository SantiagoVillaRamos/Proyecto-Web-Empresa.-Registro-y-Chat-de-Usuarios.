from django.test import TestCase
from .models import Profile
from django.contrib.auth.models import User
# Create your tests here.

# crear una prueba unitaria que se encarga de automatizar un procedimiento que se cree un usuario y luego comprobamos si se ha creado un perfil a ese propio usuario para saber si el codigo esta funcionando correctamente

class ProfileTestCase(TestCase):
    
    # en este metodo prepararemos la prueba
    def setUp(self):
        # crear un usuario de pruebas
        User.objects.create_user('test', 'test@test.com', 'test1234')
    
    # aqui tenemos la propia prueba
    def test_profile_exists(self):
        exists = Profile.objects.filter(user__username='test').exists()
        self.assertEqual(exists, True)