from django.urls import path

from app.views.Curso.views import *
from app.views.Usuario.views import *

app_name = 'app'
urlpatterns = [
    #path('Curso/',listar_curso,name="listar_curso" ),
    path('curso/',CursoListView.as_view(),name="index_curso"),
    path('curso/crear/',CursoCreateView.as_view(),name="crear_curso"),
    path('curso/editar/<int:pk>/',CursoupdateView.as_view(),name="editar_curso"),
    path('curso/eliminar/<int:pk>/',CursoDeleteView.as_view(),name="eliminar_curso"),
    path('curso/limpiar/',CursoCleandView.as_view(),name="limpiar_curso"),
    path('usuario/',UsuarioListView.as_view(),name="index_usuario"),
    path('usuario/crear/',UsuarioCreateView.as_view(),name="crear_usuario"),
    path('usuario/editar/<int:pk>/',UsuarioUpdateView.as_view(),name="editar_usuario"),
]
