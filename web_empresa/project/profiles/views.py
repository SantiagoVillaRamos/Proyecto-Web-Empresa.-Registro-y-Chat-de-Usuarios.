from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from registration.models import Profile
# Create your views here.

# vista encargada de mostrar la lista de los usuarios 
class ListsProfile(ListView):
    # modelo
    model = Profile
    template_name = 'profiles/profile_lists.html'
    paginate_by = 3


# vista que muestra el perfil especifico de cada usuario a partir de su nombre de usuario
class DetailProfile(DetailView):
    # modelo
    model = Profile
    template_name = 'profiles/profile_detail.html'
    
    # definimos el metodo get_object que recupera el perfil a partir del parametro <username> toma el nombre del perfil del usuario
    # recupera el objeto que lo estamos pasando en la parte superior del path
    def get_object(self):
        # retorna un get_object_or_404(), filtramos a partir del campo username del user y pasando como argumento el kwargs del username que hace referencia a las urls <username>/ del path.
        return get_object_or_404(Profile, user__username=self.kwargs['username'])
