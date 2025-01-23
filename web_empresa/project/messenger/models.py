from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed

# Create your m

# clase que se encarga del usuario emisor de un mensaje
class Messenger(models.Model):
    # relacion ForeignKey con los usuarios
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    # contenido del mensaje 
    content = models.TextField()
    # fecha de creacion del mensaje
    created = models.DateTimeField(auto_now_add=True)
    
    # ordenar los mensajes por fecha de creacion
    class Meta:
        ordering = ['created']
        

# clase ThreadManager(models.Manager) que hereda de models.Manager. Este es el filtro que se hacreado y se pasa al test la funcion find()
class ThreadManager(models.Manager):
    # metodo que recupera un hilo a partir de los usuarios
    def find(self, user1, user2):
        # recupera los hilos que tienen a user1 y user2
        query = self.filter(users=user1).filter(users=user2)
        # si existe el hilo lo retorna
        if len(query) > 0:
            return query[0]
        # si no existe el hilo lo crea
        return None
    
    # metodo que crea un hilo a partir de los usuarios
    def find_or_create(self, user1, user2):
        # recupera el hilo si existe
        query = self.find(user1, user2)
        # si existe el hilo es nulo lo crea
        if query is None:
            # crea el hilo vacio
            query = Thread.objects.create()
            # añadimos los dos usuarios al hilo
            query.users.add(user1, user2)
        # si no existe el hilo lo crea
        return query        


# clase que almacena los usuarios con los mensajes         
class Thread(models.Model):
    # relacion ManyToMany con los usuarios
    users = models.ManyToManyField(User, related_name='threads')
    # relacion ManyToMany con los mensajes
    messages = models.ManyToManyField(Messenger)
    # campo updated que se encarga de actualizar la fecha de actualizacion
    updated = models.DateTimeField(auto_now=True)
    
    # asignamos el ThreadManager a la clase Thread
    objects = ThreadManager()
    
    # clase meta que se encarga de ordenar los hilos por fecha de actualizacion
    class Meta:
        ordering = ['-updated']
    
    
    
# definimos la señal que se encarga de añadir los mensajes a un hilo cuando se añaden los usuarios a un hilo 
def messages_changed(sender, **kwargs):
    # instancia que esta mandando la señal 
    instance = kwargs.pop('instance', None)
    # accion que se esta realizando en la señal ya sea pre_add, post_add, pre_remove, post_remove, en este caso detectaremos el pre_add, despues de añadir los mensajes
    action = kwargs.pop('action', None)
    # conjunto de claves primarias que se estan añadiendo al hilo
    pk_set = kwargs.pop('pk_set', None)
    
    # intersectar el pk_set con los mensajes del hilo con las claves primarias de los mensajes que se han añadido al hilo y si su autor no forma parte del hilo borra el mensaje para que no se añada
    false_pk_set = set() # conjunto de claves primarias que no se añadiran al hilo
    if action is 'pre_add':
        # recorre los mensajes que se han añadido al hilo 
        for msk_pk in pk_set:
            # recupera el mensaje con la clave primaria msk_pk
            message = Messenger.objects.get(pk=msk_pk)
            # si el usuario del mensaje no esta en los usuarios del hilo que se registraron en la instancia del hilo
            if message.user not in instance.users.all():
                print('El usuario ({}) no forma parte del hilo'.format(message.user))
                # extrae y añade los mensajes fraudulentos al conjunto de claves primarias que no se añadiran al hilo
                false_pk_set.add(msk_pk)
                
    # buscar los mensajes de false_pk_set que si estan en pk_set
    pk_set.difference_update(false_pk_set)
    
    # forzar la actualizacion de los mensajes del hilo haciendo save
    instance.save()
            
# señal que se encarga de recorrer los mensajes que estan en el campo messages de la clase Thread   
m2m_changed.connect(messages_changed, sender=Thread.messages.through)