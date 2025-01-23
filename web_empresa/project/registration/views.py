# vistas para gestionar el formulario de registro
from .forms import UserCreactionFormWithEmail, ProfileForm, EmailForm
from .models import Profile
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django import forms

# vista de registro
class SignUpView(CreateView):
    form_class = UserCreactionFormWithEmail
    template_name = 'registration/signup.html'
    
    # definimos el metodo get_success_url() para mejorar el tiempo de ejecucion a este enlace
    def get_success_url(self):
        return reverse_lazy('login') + '?register'
    
    # recuperamos el formulario con el metodo get_form() para modificar su diseño
    def get_form(self, form_class =None):
        # recuperamos el formulario
        form = super(SignUpView, self).get_form()
        # Modificar el formulario en tiempo real
        form.fields['username'].widget = forms.Textarea(attrs={'class':'form-control mb-2', 'placeholder':'Nombre de Usuario', 'rows':1})
        form.fields['email'].widget = forms.EmailInput(attrs={'class':'form-control mb-2', 'placeholder':'Direccion Email'})
        form.fields['password1'].widget = forms.PasswordInput(attrs={'class':'form-control mb-2', 'placeholder':'Contraseña'})
        form.fields['password2'].widget = forms.PasswordInput(attrs={'class':'form-control mb-2', 'placeholder':'Confirmacion contraseña'})
        return form


# vista template si el usuario esta autenticado para modificar sus datos
@method_decorator(login_required, name="dispatch")
class ProfileUpdate(UpdateView):
    form_class = ProfileForm
    success_url = reverse_lazy('profile')
    template_name = 'registration/profile_form.html'
    
    # recuperar el objeto que se va a editar
    def get_object(self):
        # el metodo get_or_create() busca el objeto o lo crea si no esta
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile
    
    
# clase que edita el email
@method_decorator(login_required, name="dispatch")
class EmailFormUpdate(UpdateView):
    form_class = EmailForm
    template_name = 'registration/profile_email.html'
    
    # sobreescribimos el metodo get_success_url()
    def get_success_url(self):
        return reverse_lazy('profile') + '?update'
    
    # recuperar el usuario que esta en request
    def get_object(self):
        # retorna el usuario que queremos editar
        return self.request.user
    
    # modificammos el diseño del email en tiempo de ejecucion
    def get_form(self, form_class =None):
        # recuperamos el formulario
        form = super(EmailFormUpdate, self).get_form()
        # modificamos en tiempo de ejecucion porque el modelo User tiene sus propios diseños
        form.fields['email'].widget = forms.EmailInput(attrs={'class':'form-control mb-2', 'placeholder':'Nuevo correo electronico'})
        return form