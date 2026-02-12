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
        context['crear_url'] = reverse_lazy('app:crear_tipo')
        return context

class TipoElementoCreateView(CreateView):
    model = tipoelemento
    form_class = TipoElementoForm
    template_name = 'TipoElemento/crear.html'
    success_url = reverse_lazy('app:index_tipo')
