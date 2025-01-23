from django.contrib.auth.models import User
from django import forms

# clase que valida el email
class ValidationEmail:
    
    # funcion que valida el email
    @staticmethod
    def validation_email(email):
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('El Email ya esta registrado, intenta con otro')
        elif not email.endswith('@gmail.com') and not email.endswith('@hotmail.com'):
            raise forms.ValidationError('El Correo debe terminar en "@gmail.com" o "@hotmail.com"')
        return email
    

# clase que valida el username
class ValidationUsername:
    
    # funcion encargada de validar el username
    @staticmethod
    def validation_username(username):
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Este nombre de usuario ya existe, intenta con otro')
        return username


# clase que valida la contraseña
class ValidationPassword:
    
    # funcion encargada de validar la contraseña
    @staticmethod
    def validation_password(password):
        if User.objects.filter(password=password).exists():
            raise forms.ValidationError('Esta contraseña ya existe, intenta con otra')
        return password