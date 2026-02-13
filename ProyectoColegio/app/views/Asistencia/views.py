from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView , View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from app.models import *
from app.forms import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import connection
# Create your views here.


def index(request):
    return render(request, 'index.html')

# Ejemplo Listar_Usuarios


def listar_usuario(request):
    usuario = Usuario.objects.all()
    return render(request, 'usuario/index.html', {'usuarios': usuario})


def listar_asistencia(request):
    asistencia = Asistencia.objects.all()
    return render(request, 'asistencia/index.html', {'asistencias': asistencia})


class AsistenciaListView(ListView):
    model = Asistencia
    template_name = 'asistencia/index.html'
    context_object_name = 'asistencias'
    # Uso de DICCIONARIOS
    # Metodo Dispatch
    # @method_decorator(login_required)

    def dispatch(self, request, *args, **kwargs):
        # if request.method == "GET":
        # return redirect('app:listar_curso')
        return super().dispatch(request, *args, **kwargs)
# metodo Post

    def post(self, request, *args, **kwargs):
        pass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # Herencia por medio de super
        context['titulo'] = 'Listado de Asistencias'
        context['subtitulo'] = 'Bienvenido al listado de asistencias'
        context['crear_url'] = reverse_lazy('app:crear_asistencia')
        context['limpiar_url'] = reverse_lazy('app:limpiar_asistencia')
        context['table'] = "Asistencias"  
        return context


class AsistenciaCreateView(CreateView):
    model = Asistencia
    form_class = AsistenciaForm
    template_name = 'asistencia/crear.html'

    success_url = reverse_lazy('app:index_asistencia')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Crear Asistencia"
        context['listar_url'] = reverse_lazy('app:index_asistencia')
        context['btn_name'] = "Guardar"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Asistencia creada correctamente")
        return super().form_valid(form)


class AsistenciaupdateView(UpdateView):
    model = Asistencia
    form_class = AsistenciaForm
    template_name = 'asistencia/crear.html'
    success_url = reverse_lazy('app:index_asistencia')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Actualizar Asistencia"
        context['listar_url'] = reverse_lazy('app:index_asistencia')
        context['btn_name'] = "Actualizar"
        return context
    
    def form_valid(self, form):
        messages.success(self.request,"Asistencia actualizada correctamente")
        return super().form_valid(form)


class AsistenciaDeleteView(DeleteView):
    model = Asistencia
    template_name = 'asistencia/eliminar.html'
    success_url = reverse_lazy('app:index_asistencia')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Eliminar Asistencia"
        context['listar_url'] = reverse_lazy('app:index_asistencia')
        return context


    def form_valid(self, form):
        messages.success(self.request, "Asistencia eliminada correctamente")
        return super().form_valid(form)

class AsistenciaCleandView(View):
   def post(self, request, *args, **kwargs):
        Asistencia.objects.all().delete()
        with connection.cursor() as cursor:
            nombre_tabla = Asistencia._meta.db_table
            print(nombre_tabla)
            cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{nombre_tabla}';")
        
        messages.success(self.request, "Todas las asistencias han sido eliminadas y el ID reiniciado.")
        return redirect(reverse_lazy('app:index_asistencia'))