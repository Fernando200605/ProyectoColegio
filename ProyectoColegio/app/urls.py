from django.urls import path
from app.views import *
from django.urls import path
from app.views.Curso.views import *
from app.views.Movimiento.views import *
from app.views.Evento.views import *
from app.views.Notificacion.views import *

app_name = 'app'
urlpatterns = [
    path('vista1/',index ,name='vista1'),
    path('usuario/',listar_usuario,name="index_usuario"),
    #path('Curso/',listar_curso,name="listar_curso" ),
    path('curso/',CursoListView.as_view(),name="index_curso"),
    path('curso/crear/',CursoCreateView.as_view(),name="crear_curso"),
    path('curso/editar/<int:pk>/',CursoupdateView.as_view(),name="editar_curso"),
    path('curso/eliminar/<int:pk>/',CursoDeleteView.as_view(),name="eliminar_curso"),
    path('curso/limpiar/',CursoCleandView.as_view(),name="limpiar_curso"),
    path('movimiento/',MovimientoListView.as_view(),name="index_movimiento"),
    path('movimiento/crear/',MovimientoCreateView.as_view(),name="crear_movimiento"),
    path('movimiento/editar/<int:pk>/',MovimientoupdateView.as_view(),name="editar_movimiento"),
    path('movimiento/eliminar/<int:pk>/',MovimientoDeleteView.as_view(),name="eliminar_movimiento"),
    path('movimiento/limpiar/',MovimientoCleandView.as_view(),name="limpiar_movimiento"),
    path('evento/',EventoListView.as_view(),name="index_evento"),
    path('evento/crear/',EventoCreateView.as_view(),name="crear_evento"),
    path('evento/editar/<int:pk>/',EventoupdateView.as_view(),name="editar_evento"),
    path('evento/eliminar/<int:pk>/',EventoDeleteView.as_view(),name="eliminar_evento"),
    path('evento/limpiar/',EventoCleandView.as_view(),name="limpiar_evento"),
    path('notificacion/',NotificacionListView.as_view(),name="index_notificacion"),
    path('notificacion/crear/',NotificacionCreateView.as_view(),name="crear_notificacion"),
    path('notificacion/editar/<int:pk>/',NotificacionupdateView.as_view(),name="editar_notificacion"),
    path('notificacion/eliminar/<int:pk>/',NotificacionDeleteView.as_view(),name="eliminar_notificacion"),
    path('notificacion/limpiar/',NotificacionCleandView.as_view(),name="limpiar_notificacion"),
]

