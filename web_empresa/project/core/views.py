from django.shortcuts import render
from django.views.generic import TemplateView

# clase templateView para la vista de la pagina de inicio
class HomePageView(TemplateView):
    template_name = 'core/home.html' 
        
    # podemos utilizar el metodo get() y retornar el render de la vista con el contexto 
    def get(self, request, *args, **kwargs): # es importante pasar sus argumentos y armgumentos clave y valor, es de buena practica
        return render(request, self.template_name, {'title': 'Mi super web', 'message': 'CBV, autenticación, registros, perfiles y más'})

# clase templateView para la vista de la pagina de ejemplo
class SamplePageView(TemplateView):
    template_name = 'core/sample.html'

    # metodo para obtener el contexto de la vista
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Página de prueba'
        context['message'] = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce hendrerit nibh vel faucibus auctor. Phasellus non arcu dictum, porttitor orci sed, maximus ligula. Duis mollis pulvinar tempor. Cras ex nisl, fringilla ut rhoncus a, vestibulum ac turpis.'
        return context
