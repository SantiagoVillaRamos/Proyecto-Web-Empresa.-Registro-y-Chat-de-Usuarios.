from .models import Page
from .forms import PageForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.shortcuts import redirect


# vista lista basada en clases encargada de listar los objetos
class PagesListView(ListView):
    model = Page
    template_name = 'pages/pages.html'

    
# vista detalle basada en clases encargada de mostrar un objeto
class PageDetailView(DetailView):
    model = Page
    template_name = 'pages/page.html'
    
    
# vista createdView basada en clases encargada de crear las paginas
@method_decorator(staff_member_required, name='dispatch')
class PageCreateView(CreateView):
    model = Page
    form_class = PageForm
    template_name = 'pages/page_form.html'
    success_url = reverse_lazy('pages:pages')


# vista updateView basada en clases encargada de actualizar las paginas
@method_decorator(staff_member_required, name='dispatch')
class PageUpdateView(UpdateView):
    model = Page
    form_class = PageForm
    template_name = 'pages/page_form_update.html' 
    
    # metodo get_success_url para redirigir a la misma pagina con un ok en la url
    def get_success_url(self):
        return reverse_lazy('pages:update', args=[self.object.id]) + '?ok'
    

# vista deleteView basada en clases encargada de eliminar las paginas
@method_decorator(staff_member_required, name='dispatch')
class PageDeleteView(DeleteView):
    model = Page
    template_name = 'pages/page_delete.html'
    success_url = reverse_lazy('pages:pages')