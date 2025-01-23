from django.test import TestCase
from django.contrib.auth.models import User
from .models import Thread, Messenger
# Create your tests here.

# ejecutamos con un py manage.py test messenger
# tener en cuenta que para cada test independiente se ejecuta de nuevo el setUp()

# clase con los test
class ThreadTestCascade(TestCase):
    
    # preparar el entorno de pruebas
    def setUp(self):
        # se crean los usuarios de prueba
        self.user1 = User.objects.create_user('user1', None, 'test1234')
        self.user2 = User.objects.create_user('user2', None, 'test1234')
        self.user3 = User.objects.create_user('user3', None, 'test1234')
        
        # crea el hilo donde se añaden los usuarios y los mensajes
        self.thread = Thread.objects.create()
    
    
    # crear test de pruebas
    # test que añade usuarios
    def test_add_user_to_thread(self):
        # añade a la relacion ManyToMany los usuarios que esta esperando
        self.thread.users.add(self.user1, self.user2)
        # test que se encara de verificar si se añadieron correctamente
        # utilizamos len() para verificar que se añadieron 2 usuarios dentro del hilo
        self.assertEqual(len(self.thread.users.all()), 2)
        
        
    # test que recupera un hilo a partir de sus usuarios
    def test_filter_thread_by_users(self):
        # añadimos los usuarios
        self.thread.users.add(self.user1, self.user2)
        # recuperar el hilo a partir de los dos usuarios
        threads = Thread.objects.filter(users=self.user1).filter(users=self.user2)
        # verificamos con asserTequal() el hilo que esta en self.thread con el hilo que tenemos en la lista threads en la primera posicion
        self.assertEqual(self.thread, threads[0])
        
        
    # caso contrario: comprobar que no exista un hilo cuando los usuarios no forman parte de el
    def test_filter_non_existent_thread(self):
        # no añadimos usuarios, si no se añaden usuarios a un hilo he intentamos recuperarlo no va a existir
        threads = Thread.objects.filter(users=self.user1).filter(users=self.user2)
        # verificamos 
        self.assertEqual(len(threads), 0)   
        
        
    # test que añade los mensajes y verifican que se añadan
    def test_add_messenger_to_thread(self):
        # añadimos los usuarios al hilo
        self.thread.users.add(self.user1, self.user2)
        # crear el mensaje con el usuario y el contenido
        messege1 = Messenger.objects.create(user=self.user1, content='Muy buenas tardes')
        messege2 = Messenger.objects.create(user=self.user2, content='Hola')
        # añadir los mensajes
        self.thread.messages.add(messege1, messege2)
        # verificamos que se hayan añadido los dos mensajes comparando la longitud
        self.assertEqual(len(self.thread.messages.all()), 2)
        
        for message in self.thread.messages.all():
            print("({}): {}".format(message.user, message.content))
            
            
    # FALLO DE SEGURIDAD: un usuario que no forma parte del hilo
    def test_add_message_from_user_not_in_thread(self):
        # añadimos los usuarios
        self.thread.users.add(self.user1, self.user2)
        # crear varios mensajes
        messege1 = Messenger.objects.create(user=self.user1, content='Muy buenas tardes')
        messege2 = Messenger.objects.create(user=self.user2, content='Hola')
        messege3 = Messenger.objects.create(user=self.user3, content='Soy un espia')
        # añadir al hilo los tres mensajes
        self.thread.messages.add(messege1, messege2, messege3)
        # verificamos que solo hayan dos mensajes
        self.assertEqual(len(self.thread.messages.all()), 2)
        
        # REFACTORIZACION:Necesitamos modificar el comportamiento del campo ManyToManyFields para que compruebe que los menssajes solo se añadan si los usuarios que los han creado forman parte del hilo.
        # para ello utilizamos una señal de django llamada m2m_changed que se encarga de gestionar los cambios en los campos ManyToManyFields.
        
        
    # buscar un hilo con el custom_manager. En vez de utilizar el manager por defecto que es filter utilizamos un manager personalizado que es find()
    def test_find_thread_custom_manager(self):
        # añadimos los usuarios
        self.thread.users.add(self.user1, self.user2)
        # recuperamos el hilo con el custom_manager que hemos creado en los modelos
        thread = Thread.objects.find(self.user1, self.user2)
        # verificamos que el hilo recuperado sea igual al hilo que hemos creado
        self.assertEqual(self.thread, thread)
        
        
    # buscar un hilo con el custom_manager. En vez de utilizar el manager por defecto que es filter utilizamos un manager personalizado que es find_or_create()
    def test_find_or_create_thread_custom_manager(self):
        # añadimos los usuarios
        self.thread.users.add(self.user1, self.user2)
        # recuperamos el hilo con el custom_manager que hemos creado en los modelos
        thread = Thread.objects.find_or_create(self.user1, self.user2)
        # verificamos que el hilo recuperado sea igual al hilo que hemos creado
        self.assertEqual(self.thread, thread)
        # recuperamos el hilo con el custom_manager que hemos creado en los modelos o que no exista
        thread = Thread.objects.find_or_create(self.user1, self.user3)  
        # verificamos que el hilo no sea nulo
        self.assertIsNotNone(thread)