from django.urls import path
from app.views.Curso.views import *
from app.views.Inventario.views import *
from app.views.Marca.views import *
from app.views.TipoElemento.views import *  
from app.views.UnidadMedida.views import *
from app.views.Categoria.views import CategoriaCreateView 

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
    path('inventario/',InventarioListView.as_view(),name="index_inventario"),
    path('inventario/crear/',ElementoCreateView.as_view(),name="crear_elemento"),
    path('inventario/editar/<int:pk>/',ElementoUpdateView.as_view(),name="editar_elemento"),
    path('inventario/eliminar/<int:pk>/',ElementoDeleteView.as_view(),name="eliminar_elemento"),
    path('inventario/limpiar/',InventarioCleanView.as_view(),name="limpiar_inventario"),
    # MARCA
    path('marca/', marcaListView.as_view(), name='index_marca'),
    path('marca/crear/', marcaCreateView.as_view(), name='crear_marca'),

    # TIPO DE ELEMENTO
    path('tipo/', TipoElementoListView.as_view(), name='index_tipo'),
    path('tipo/crear/', TipoElementoCreateView.as_view(), name='crear_tipo'),

    # UNIDAD DE MEDIDA
    path('unidad/', UnidadMedidaListView.as_view(), name='index_unidad'),
    path('unidad/crear/', UnidadMedidaCreateView.as_view(), name='crear_unidad'),
    path('unidad/editar/<int:pk>/', UnidadMedidaUpdateView.as_view(), name='editar_unidad'),
    path('unidad/eliminar/<int:pk>/', UnidadMedidaDeleteView.as_view(), name='eliminar_unidad'),

    path('tipo/crear/', TipoElementoCreateView.as_view(), name='crear_tipoelemento'),
    path('marca/crear/', marcaCreateView.as_view(), name='crear_marca'),
    path('unidad/crear/', UnidadMedidaCreateView.as_view(), name='crear_unidad'),
    path('categoria/crear/', CategoriaCreateView.as_view(), name='crear_categoria'),

]
