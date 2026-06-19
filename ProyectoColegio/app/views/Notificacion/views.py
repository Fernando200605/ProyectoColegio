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

# Ejemplo Listar_UsuarioS
def listar_usuario(request):
    usuario = Usuario.objects.all()
    return render(request, 'usuario/index.html', {'usuarios': usuario})


def listar_notificacion(request):
    notificacion = Notificacion.objects.all()
    return render(request, 'notificacion/index.html', {'notificaciones': notificacion})


class NotificacionListView(ListView):
    model = Notificacion
    template_name = 'notificacion/index.html'
    context_object_name = 'notificacion'

    def dispatch(self, request, *args, **kwargs):
        # if request.method == "GET":
        # return redirect('app:listar_curso')
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        usuario = self.request.user
        rol = usuario.get_rol()
        if rol == "Administrador":
            return Notificacion.objects.all()
        else:
            return Notificacion.objects.filter(receptor=usuario.id)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from django.utils import timezone as tz
        usuario = self.request.user
        rol = usuario.get_rol()
        qs = self.get_queryset()
        total = qs.count()
        no_leidas = qs.filter(estado="no_leida").count()
        urgentes = qs.filter(tipo="urgente").count()

        context['titulo'] = 'Listado de Notificaciones'
        context['subtitulo'] = 'Centro de notificaciones del sistema'
        context['crear_url'] = reverse_lazy('app:crear_notificacion')
        context['limpiar_url'] = reverse_lazy('app:limpiar_notificacion')
        context['total_count'] = total
        context['total_text'] = "Total de Notificaciones"
        context['text'] = "Sin leer"
        context['low_stock'] = no_leidas
        context['icon_primary'] = "fa-bell"
        context['icon_secodary'] = "fa-envelope"
        context['urgentes'] = urgentes
        user = self.request.user
        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name
        context['puede_crear'] = user.has_perm(f'{app_label}.add_{model_name}')
        context['puede_editar'] = user.has_perm(f'{app_label}.change_{model_name}')
        context['puede_eliminar'] = user.has_perm(f'{app_label}.delete_{model_name}')
        return context


class NotificacionCreateView(CreateView):
    model = Notificacion
    form_class = NotificacionForm
    template_name = 'notificacion/crear.html'

    success_url = reverse_lazy('app:index_notificacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Crear notificacion"
        context['listar_url'] = reverse_lazy('app:index_notificacion')
        context['btn_name'] = "Guardar"
        return context

    def form_valid(self, form):
        messages.success(self.request, "notificacion creada correctamente")
        return super().form_valid(form)


class NotificacionupdateView(UpdateView):
    model = Notificacion
    form_class = NotificacionForm
    template_name = 'notificacion/crear.html'
    success_url = reverse_lazy('app:index_notificacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Actualizar Notificacion"
        context['listar_url'] = reverse_lazy('app:index_notificacion')
        context['btn_name'] = "Actualizar"
        return context
    
    def form_valid(self, form):
        messages.success(self.request,"notificacion actualizada correctamente")
        return super().form_valid(form)


class NotificacionDeleteView(DeleteView):
    model = Notificacion
    template_name = 'notificacion/eliminar.html'
    success_url = reverse_lazy('app:index_notificacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Eliminar notificacion"
        context['listar_url'] = reverse_lazy('app:index_notificacion')
        return context


    def form_valid(self, form):
        messages.success(self.request, "notificacion eliminada correctamente")
        return super().form_valid(form)

class NotificacionCleandView(View):
   def post(self, request, *args, **kwargs):
        Notificacion.objects.all().delete()
        with connection.cursor() as cursor:
            nombre_tabla = Notificacion._meta.db_table
            print(nombre_tabla)
            cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{nombre_tabla}';")
        
        messages.success(self.request, "Todas las notificaciones han sido eliminados y el ID reiniciado.")
        return redirect(reverse_lazy('app:index_notificacion')) 