from django.urls import path
from app.views import *
app_name = 'app'
urlpatterns = [
    path('vista1/',index ,name='vista1'),
    path('usuario/',listar_usuario,name="index_usuario"),
]
