from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from app.models import Usuario,Asistencia,Elemento,Notificacion
from django.urls import reverse_lazy
from app.mixins import RolMixin
from django.db.models.functions import TruncDate
from django.db.models import Count ,Sum
from django.utils.timezone import now
from datetime import timedelta
from django.views import View
from django.http import JsonResponse
import json
from django.shortcuts import render
class DashboardView(LoginRequiredMixin,RolMixin, TemplateView):
    template_name = 'index/dashboard.html'
    login_url = reverse_lazy('app:login')
    roles_permitidos = ['Administrador', 'Docente']
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['usuario_nombre'] = user.nombre
        context['usuario_rol'] = user.get_rol()
        context['usuario_estado'] = 'Activo' if user.estado else 'Inactivo'
        hoy = now().date()
        inicio = hoy - timedelta(days=6)
        datos = (
            Asistencia.objects
            .filter(fecha__range=[inicio,hoy])
            .values('fecha')
            .annotate(total=Count('id'))
            .order_by('fecha')
		)
        print(datos)
        labels = []
        data = []
        for item in datos:
            if item['fecha']:
                labels.append(item['fecha'].strftime('%d %b'))
                data.append(item['total'])
        context['labels'] = json.dumps(labels)
        context['data'] = json.dumps(data)
        
        datos_inventario = (
            Elemento.objects
            .values('categoriaId__nombre')
            .annotate(total = Sum('stockActual'))
            .order_by('categoriaId__nombre')
		)
        labels_Elemento = []
        datos_Elemento =  []
        print(datos_inventario)
        for item in datos_inventario:
            labels_Elemento.append(item['categoriaId__nombre'])
            datos_Elemento.append(item['total'])
        context['labels_elemento'] = json.dumps(labels_Elemento)
        context['datos_elemento'] = json.dumps(datos_Elemento)
        return context

class Qr_code(TemplateView):
    template_name = "escaner/escaner.html"
    

class NotificacionesView(LoginRequiredMixin, View):
    template_name = "modals/modals_notificaciones.html"

    def get(self, request):
        notificaciones = Notificacion.objects.filter(
            receptor_id=request.user
        ).order_by('-fecha_envio')

        return render(request, self.template_name, {
            'notificaciones': notificaciones
        })