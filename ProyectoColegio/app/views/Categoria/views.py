from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from app.models import categoria
from app.forms import CategoriaForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import connection


class CategoriaCreateView(CreateView):
    model = categoria
    form_class = CategoriaForm
    template_name = 'Categoria/crear.html'
    success_url = reverse_lazy('app:crear_elemento')  # cambia si tu listado tiene otro nombre

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Crear Categoría"
        context['listar_url'] = reverse_lazy('app:crear_elemento')
        context['btn_name'] = "Guardar"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Categoría creada correctamente")
        return super().form_valid(form)