from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from app.models import tipoelemento
from app.forms import TipoElementoForm
from django.urls import reverse_lazy
from django.contrib import messages

class TipoElementoListView(ListView):
    model = tipoelemento
    template_name = 'TipoElemento/index.html'
    context_object_name = 'tipos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Tipos de Elemento'
        context['subtitulo'] = 'Clasificación de inventario'
        context['crear_url'] = reverse_lazy('app:crear_elemento')
        return context
    
class TipoElementoCreateView(CreateView):
    model = tipoelemento
    form_class = TipoElementoForm
    template_name = 'TipoElemento/crear.html'
    success_url = reverse_lazy('app:index_tipo')
    
    def form_valid(self, form):
        messages.success(self.request, 'Se creo un nuevo tipo de elemento')
        return super().form_valid(form)
    

class TipoElementoUpdateView(UpdateView):
    model = tipoelemento
    form_class = TipoElementoForm
    template_name = 'TipoElemento/crear.html'
    success_url = reverse_lazy('app:index_tipo')
    
    def form_valid(self, form):
        messages.success(self.request, 'Se actualizo con exito')
        return super().form_valid(form)

class TipoElementoDeleteView(DeleteView):
    model = tipoelemento
    template_name = 'TipoElemento/eliminar.html'
    success_url = reverse_lazy('app:index_tipo')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Tipo De Elemento'
        context['subtitulo'] = '¿Está seguro de eliminar este Tipo De Elemento?'
        context['listar_url'] = reverse_lazy('app:index_usuario')
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Tipo de elemento  eliminado exitosamente.')
        return super().form_valid(form)
    
    success_url = reverse_lazy('app:crear_elemento')
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['listar_url'] = reverse_lazy('app:crear_elemento')
        return context
