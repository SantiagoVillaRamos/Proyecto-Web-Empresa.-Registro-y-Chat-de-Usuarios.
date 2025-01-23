from django import forms
from .models import Page

# Formulario para crear una pagina
class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['title', 'content', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título de la página'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Contenido de la página', 'rows': 2}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Orden de la página'}),
        }
        labels = {
            'title': '',
            'content': '',
            'order': 'Orden',
        }