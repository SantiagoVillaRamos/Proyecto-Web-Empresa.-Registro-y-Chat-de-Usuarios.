from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.http import Http404
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Thread
from django.contrib.auth.models import User
# importamos JSON response para generar la respuesta en formato JSON
from django.http import JsonResponse


# verificamos que el usuario este autenticado
# vista que muestra los hilos de un usuario
@method_decorator(login_required, name='dispatch')
class ThreadsListView(TemplateView):
    # template que se encarga de mostrar la lista de hilos
    template_name = 'messenger/thread_list.html'


# vista que muestra un hilo con la conversacion
# vista que muestra los mensajes de un hilo
@method_decorator(login_required, name='dispatch')
class ThreadDetailView(DetailView):
    model = Thread
    template_name = 'messenger/thread_detail.html'

    # sobreescribimos el metodo get_queryset() para filtrar los mensajes de un hilo
    def get_object(self):
        # recuperamos el hilo
        obj = super(ThreadDetailView, self).get_object()
        # validamos si el usuario no esta en los usuarios registrados
        if self.request.user not in obj.users.all():
            # si no esta en los usuarios registrados retornamos un Http 404
            raise Http404()
        # retornamos el obj
        return obj
        
        
# vista que añade un mensaje
def add_messenger(request, pk): # se declara resquest porque hay esta el usuario identificado y le pasamos un pk
    # Da a entender que cuando añadamos un mensaje devolveremos una respuesta 
    json_response = {'create':False}
    # verificamos si el usuario esta autenticado
    if request.user.is_authenticated:
        # recuperamos el contenido
        content = request.GET.get('content', None)
        # si el contenido existe
        if content:
            # recuperamos el hilo
            thread = get_object_or_404(Thread, pk=pk)
            # creamos el mensaje
            message = thread.messages.create(user=request.user, content=content)
            # añadir al hilo el mensaje
            thread.messages.add(message)
            # cambiar el diccionario json_response a true
            json_response['created'] = True
            # si la longitud de los mensajes es 1:
            if len(thread.messages.all()) is 1:
                # crear una nueva clave en el diccionario json_response
                json_response['first'] = True
    else:
        # si el usuario no esta autenticado retornamos un Http 404
        return Http404("Usuario no autenticado")
    # retornamos la respuesta en formato JSON 
    return JsonResponse(json_response) # retornamos la respuesta en formato JSON


# vista que establece una conversacion privada con otro usuario
@login_required # verificamos que el usuario este autenticado
def start_thread(request, username):
    # recuperamos el usuario
    user = get_object_or_404(User, username=username)
    # creamos el hilo
    thread = Thread.objects.find_or_create(user, request.user)
    # redirigimos a la vista de detalle del hilo
    return redirect(reverse_lazy('messenger:detail', args=[thread.pk]))