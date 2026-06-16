from django.shortcuts import render, redirect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View,
)
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from app.models import *
from app.forms import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import connection
from app.google_api import obtener_servicio, crear_evento, actualizar_evento,eliminar_evento
from datetime import datetime, timedelta
from django.http import JsonResponse

# Create your views here.

from googleapiclient.errors import HttpError


class EventoListView(ListView):
    model = Evento
    template_name = "evento/index.html"
    context_object_name = "eventos"
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
        context = super().get_context_data(**kwargs)
        from django.utils import timezone as tz
        hoy = tz.now()
        total = Evento.objects.count()
        proximos = Evento.objects.filter(fecha_inicio__gte=hoy).count()
        pasados = Evento.objects.filter(fecha_fin__lt=hoy).count()

        context["titulo"] = "Listado de Eventos"
        context["subtitulo"] = "Calendario de actividades del colegio"
        context["crear_url"] = reverse_lazy("app:crear_evento")
        context["limpiar_url"] = reverse_lazy("app:limpiar_evento")
        context["total_count"] = total
        context["total_text"] = "Total de Eventos"
        context["text"] = "Próximos eventos"
        context["low_stock"] = proximos
        context["icon_primary"] = "fa-calendar-alt"
        context["icon_secodary"] = "fa-calendar-check"
        context["pasados"] = pasados
        user = self.request.user
        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name
        context["puede_crear"] = user.has_perm(f"{app_label}.add_{model_name}")
        context["puede_editar"] = user.has_perm(f"{app_label}.change_{model_name}")
        context["puede_eliminar"] = user.has_perm(f"{app_label}.delete_{model_name}")
        return context


class EventoCreateView(CreateView):
    model = Evento
    form_class = EventoForm
    template_name = "evento/crear.html"

    success_url = reverse_lazy("app:index_evento")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Crear Evento"
        context["listar_url"] = reverse_lazy("app:index_evento")
        context["btn_name"] = "Guardar"
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        evento = self.object
        try:
            evento_google = crear_evento(
                evento.titulo, evento.descripcion, evento.fecha_inicio, evento.fecha_fin
            )
            if evento_google:
                evento.google_event_id = evento_google["id"]
                evento.save()
        except Exception as e:
            print("Error en Google Calendar : ", e)
        messages.success(self.request, "Evento Creado Correctamente")
        return response


class EventoupdateView(UpdateView):
    model = Evento
    form_class = EventoForm
    template_name = "evento/crear.html"
    success_url = reverse_lazy("app:index_evento")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Actualizar Evento"
        context["listar_url"] = reverse_lazy("app:index_evento")
        context["btn_name"] = "Actualizar"
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        evento = self.object

        actualizar_evento(
            evento.google_event_id,
            evento.titulo,
            evento.descripcion,
            evento.fecha_inicio,
            evento.fecha_fin,
        )
        messages.success(self.request,'Evento Actualizado Correctamente')
        return response


class EventoDeleteView(DeleteView):
    model = Evento
    template_name = "evento/eliminar.html"
    success_url = reverse_lazy("app:index_evento")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Eliminar Evento"
        context["listar_url"] = reverse_lazy("app:index_evento")
        return context

    def form_valid(self, form):
        evento = self.get_object()
        try:
            if evento.google_event_id:
                eliminar_evento(evento.google_event_id)
        except Exception as e:
            print("Error en el google Calendar",e)
        messages.success(self.request, "Evento eliminado correctamente")
        return super().form_valid(form)


class EventoCleandView(View):
    def post(self, request, *args, **kwargs):
        Evento.objects.all().delete()
        with connection.cursor() as cursor:
            nombre_tabla = Evento._meta.db_table
            print(nombre_tabla)
            cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{nombre_tabla}';")

        messages.success(
            self.request, "Todos los Eventos han sido eliminados y el ID reiniciado."
        )
        return redirect(reverse_lazy("app:index_evento"))


def listar_eventos(request):

    try:

        servicio = obtener_servicio()

        ahora = datetime.utcnow().isoformat() + "Z"

        eventos_resultado = (
            servicio.events()
            .list(
                calendarId="primary",
                timeMin=ahora,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )

        eventos = eventos_resultado.get("items", [])

        lista = []

        for evento in eventos:

            inicio = evento["start"].get("dateTime", evento["start"].get("date"))

            fin = evento["end"].get("dateTime", evento["end"].get("date"))

            lista.append(
                {
                    "titulo": evento.get("summary"),
                    "descripcion": evento.get("description"),
                    "inicio": inicio,
                    "fin": fin,
                }
            )

        return JsonResponse({"eventos": lista})

    except HttpError as error:

        return JsonResponse({"error": str(error)}, status=500)
