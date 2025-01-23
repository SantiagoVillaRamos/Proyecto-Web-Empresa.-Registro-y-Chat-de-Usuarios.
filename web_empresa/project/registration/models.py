from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# sobre-escribir el metodo upload_to='media' que guardara la imagen reciente y borrara la antigua
def custom_upload_to(instance, filename):
    # recuperamos la instancia justo como estaba antes de guardarla
    old_instance = Profile.objects.get(pk=instance.pk)
    # accedemos al avatar que teniamos antes y con el metodo delete() se borraran automaticamente
    old_instance.avatar.delete() 
    # retornamos media y le indicamos el nombre del fichero filename
    return 'media/' + filename


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to = custom_upload_to, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    link = models.URLField(max_length=200, null=True, blank=True)
    
    class Meta:
       verbose_name = 'perfil'
       verbose_name_plural = 'perfiles'
       # ordena los objetos a partir del nombre del usuario
       ordering = ['user__username']
            
    def __str__(self):
        return self.user.username
    
    
# crear una señasl que se encargara de crear automaticamente un perfil justo despues que se cree un usuario
@receiver(post_save, sender=User)
def ensure_profile_exists(sender, instance, **kwargs):
    if kwargs.get('created', False):
        Profile.objects.get_or_create(user=instance)
        #print("Se acaba de crear un usuario y su perfil enlazado")