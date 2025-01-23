from django import forms
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .class_forms.valitation.class_validation_form import ValidationPassword, ValidationEmail, ValidationUsername


# clase formulario registro
class UserCreactionFormWithEmail(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text='Requerido, 254 caracteres como maximo y debe ser requerido'
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
    # metodo clean_email() que valida si ya existe el email de lo contrario muestra un error
    def clean_email(self):
        email = self.cleaned_data.get('email')
        return ValidationEmail.validation_email(email)
    
    # metodo clean_username() encargado de validar que no haya otro nombre
    def clean_username(self):
        username = self.cleaned_data.get('username')
        return ValidationUsername.validation_username(username)
    
    # metodo encargado de validar que la contraseña no exista
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        return ValidationPassword.validation_password(password1)


# formulario editar perfil del usuario
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar','bio','link']
        widgets = {
            'avatar': forms.ClearableFileInput(
                attrs={'class':'form-control-file mt-3'}
            ),
            'bio': forms.Textarea(
                attrs={'class':'form-control mt-3', 'rows':3, 'placeholder':'Biografia'}
            ),
            'link': forms.URLInput(
                attrs={'class':'form-control mt-3', 'placeholder':'Enlace'}
            ),
        }
        
# formulario para editar el email
class EmailForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        help_text='Requerido, 254 caracteres como maximo y debe ser requerido'
    )
    
    class Meta:
        model = User
        fields = ['email']

    # metodo clean_email() que valida si ya existe el email de lo contrario muestra un error
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if 'email' in self.cleaned_data:
            return ValidationEmail.validation_email(email)