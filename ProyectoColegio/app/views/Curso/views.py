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
from django.http import Http404
# Create your views here.
from django.contrib.auth.mixins import PermissionRequiredMixin


def index(request):
    return render(request, 'index.html')

# Ejemplo Listar_Usuarios


def listar_usuario(request):
    usuario = Usuario.objects.all()
    return render(request, 'usuario/index.html', {'usuarios': usuario})


def listar_curso(request):
    curso = Curso.objects.all()
    return render(request, 'curso/index.html', {'cursos': curso})


from django.views.generic import ListView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy

class CursoListView(PermissionRequiredMixin, ListView):
    model = Curso
    template_name = 'curso/index.html'
    context_object_name = 'cursos'
    permission_required = 'app.view_curso'
    raise_exception = True

    def handle_no_permission(self):
        raise Http404("No se encontro la paginas")

    def get_queryset(self):
        user = self.request.user
        rol = user.get_rol()
        if rol == "Administrador":
            return Curso.objects.select_related("docenteid__usuario").all()
        else:
            return Curso.objects.filter(docenteid__usuario=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        rol = user.get_rol()

        if rol != "Administrador":
            curso = Curso.objects.filter(docenteid__usuario=user).first()
            context['curso'] = curso
            context['estudiantes'] = curso.estudiante_set.all() if curso else []
            context['titulo'] = 'Listado de Estudiantes'
            context['subtitulo'] = 'Bienvenido al listado de estudiantes de tu curso'
            context['text'] = "Estudiantes inscritos en tu curso"
            context['total_text'] = "Total de Estudiantes"
            context['total_count'] = context['estudiantes'].count()
            context['low_stock'] = context['estudiantes'].filter(estadoMatricula="No Matriculado").count()
            context['icon_primary'] = "fa-user-graduate"
            context['icon_secodary'] = "fa-user-times"
        else:
            total_cursos = Curso.objects.count()
            total_estudiantes = Estudiante.objects.count()
            context['titulo'] = 'Listado de Cursos'
            context['subtitulo'] = 'Gestión de cursos del colegio'
            context['crear_url'] = reverse_lazy('app:crear_curso')
            context['limpiar_url'] = reverse_lazy('app:limpiar_curso')
            context['text'] = "Total de Estudiantes"
            context['total_text'] = "Total de Cursos"
            context['total_count'] = total_cursos
            context['low_stock'] = total_estudiantes
            context['icon_primary'] = "fa-graduation-cap"
            context['icon_secodary'] = "fa-users"

        # 🔹 PERMISOS DINÁMICOS
        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name

        context['puede_crear'] = user.has_perm(f'{app_label}.add_{model_name}')
        context['puede_editar'] = user.has_perm(f'{app_label}.change_{model_name}')
        context['puede_eliminar'] = user.has_perm(f'{app_label}.delete_{model_name}')

        context['icon_primary'] = "fa-arrow-up"
        context['icon_secodary'] = "fa-arrow-down"
        context['rol'] = rol
        context['modo'] = 'cursos' if rol == "Administrador" else 'estudiantes'

        return context

class CursoCreateView(PermissionRequiredMixin,CreateView):
    model = Curso
    form_class = CursoForm
    template_name = 'curso/crear.html'    
    success_url = reverse_lazy('app:index_curso')
    permission_required = 'app.add_curso'
    raise_exception = True
    def handle_no_permission(self):
        raise Http404("No se encontro la paginas")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Crear Curso"
        context['listar_url'] = reverse_lazy('app:index_curso')
        context['btn_name'] = "Guardar"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Curso creado correctamente")
        return super().form_valid(form)


class CursoupdateView(PermissionRequiredMixin,UpdateView):
    model = Curso
    form_class = CursoForm
    template_name = 'curso/crear.html'
    success_url = reverse_lazy('app:index_curso')
    permission_required = 'app.change_curso'
    raise_exception = True

    def handle_no_permission(self):
        raise Http404("No se encontro la paginas")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Actualizar Curso"
        context['listar_url'] = reverse_lazy('app:index_curso')
        context['btn_name'] = "Actualizar"
        return context
    
    def form_valid(self, form):
        messages.success(self.request,"Curso actualizado correctamente")
        return super().form_valid(form)


class CursoDeleteView(DeleteView):
    model = Curso
    template_name = 'curso/eliminar.html'
    success_url = reverse_lazy('app:index_curso')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Eliminar Curso"
        context['listar_url'] = reverse_lazy('app:index_curso')
        return context


    def form_valid(self, form):
        messages.success(self.request, "Curso eliminado correctamente")
        return super().form_valid(form)

class CursoCleandView(View):
   def post(self, request, *args, **kwargs):
        Curso.objects.all().delete()
        with connection.cursor() as cursor:
            nombre_tabla = Curso._meta.db_table
            print(nombre_tabla)
            cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{nombre_tabla}';")
        
        messages.success(self.request, "Todos los cursos han sido eliminados y el ID reiniciado.")
        return redirect(reverse_lazy('app:index_curso'))