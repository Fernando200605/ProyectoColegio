from django.views.generic import CreateView
from django.shortcuts import redirect
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from app.models import *
from app.forms import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import connection
from django.utils import timezone
from django.http import JsonResponse


class UsuarioListView(ListView):
    model = Usuario
    template_name = 'usuario/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Usuarios'
        context['subtitulo'] = 'Bienvenido al listado de usuarios'
        context['crear_url'] = reverse_lazy('app:crear_usuario')
        context['limpiar_url'] = reverse_lazy('app:limpiar_usuario')
        return context


class UsuarioCreateView(CreateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'usuario/crear.html'
    success_url = reverse_lazy('app:index_usuario')

    def form_valid(self, form):
        usuario = form.save(commit=False)
        usuario.contraseña = form.cleaned_data['contraseña']

        usuario.save()

        rol = self.request.POST.get('rol')

        if rol == 'administrador':
            Administrador.objects.create(
                usuario=usuario, cargo='Administrador'
            )

        elif rol == 'docente':
            docente.objects.create(usuario=usuario
            )
        elif rol == 'acudiente':
            Acudiente.objects.create(usuario=usuario)

        messages.success(self.request, 'Usuario creado exitosamente.')
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Usuario'
        context['subtitulo'] = 'Complete el formulario para crear un nuevo usuario'
        context['listar_url'] = reverse_lazy('app:index_usuario')
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Usuario'
        context['subtitulo'] = 'Complete el formulario para crear un nuevo usuario'
        context['listar_url'] = reverse_lazy('app:index_usuario')
        return context


class UsuarioUpdateView(UpdateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'usuario/crear.html'
    success_url = reverse_lazy('app:index_usuario')

    def form_valid(self, form):
        usuario = form.save(commit=False)

        nueva_contraseña = form.cleaned_data.get('contraseña')
        if nueva_contraseña:
            usuario.contraseña = nueva_contraseña

        usuario.save()

        rol = self.request.POST.get('rol')

        Administrador.objects.filter(usuario=usuario).delete()
        docente.objects.filter(usuario=usuario).delete()
        Acudiente.objects.filter(usuario=usuario).delete()

        if rol == 'administrador':
            Administrador.objects.create(
                usuario=usuario, cargo='Administrador')
        elif rol == 'docente':
            docente.objects.create(usuario=usuario)
        elif rol == 'acudiente':
            Acudiente.objects.create(usuario=usuario)

        messages.success(self.request, 'Usuario actualizado exitosamente.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.object

        if Administrador.objects.filter(usuario=usuario).exists():
            context['rol_actual'] = 'administrador'
        elif docente.objects.filter(usuario=usuario).exists():
            context['rol_actual'] = 'docente'
        elif Acudiente.objects.filter(usuario=usuario).exists():
            context['rol_actual'] = 'acudiente'
        else:
            context['rol_actual'] = ''

        context['titulo'] = 'Editar Usuario'
        context['subtitulo'] = 'Complete el formulario para editar el usuario'
        context['listar_url'] = reverse_lazy('app:index_usuario')
        return context


class UsuarioDeleteView(DeleteView):
    model = Usuario
    template_name = 'usuario/eliminar.html'
    success_url = reverse_lazy('app:index_usuario')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Usuario'
        context['subtitulo'] = '¿Está seguro de eliminar este usuario?'
        context['listar_url'] = reverse_lazy('app:index_usuario')
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Usuario eliminado exitosamente.')
        return super().form_valid(form)

class UsuarioDetailView(View):
    def get(self, request, pk):
        usuario = Usuario.objects.get(pk=pk)

        data = {
            'nombre': usuario.nombre,
            'email': usuario.email,
            'rol': str(usuario.get_rol()),
            'estado': 'Activo' if usuario.estado else 'Inactivo',
        }

        return JsonResponse(data)

class UsuarioCleandView(View):
       def post(self, request, *args, **kwargs):
        Usuario.objects.all().delete()
        with connection.cursor() as cursor:
            nombre_tabla = Usuario._meta.db_table
            cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{nombre_tabla}';")
        
        messages.success(self.request, "Todos los Usuarips han sido eliminados y el ID reiniciado.")
        return redirect(reverse_lazy('app:index_usuario'))