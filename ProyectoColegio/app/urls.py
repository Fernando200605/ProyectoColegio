from django.urls import path
from app.views.Curso.views import *
from app.views.Asistencia.views import *

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
    path("asistencia/", AsistenciaListView.as_view(), name="index_asistencia"),
    path('asistencia/crear/', AsistenciaCreateView.as_view(), name="crear_asistencia"),
    path("asistencia/editar/<int:pk>/", AsistenciaupdateView.as_view(), name="editar_asistencia"),
    path('asistencia/eliminar/<int:pk>/',AsistenciaDeleteView.as_view(),name="eliminar_asistencia"),
    path('asistencia/limpiar/',AsistenciaCleandView.as_view(),name="limpiar_asistencia"),
]
