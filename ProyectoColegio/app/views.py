from django.shortcuts import render , redirect
from .models import *
# Create your views here.

def index(request):
        return render(request, 'index.html')

#Ejemplo Listar_Usuarios
def listar_usuario(request):
        usuario = Usuario.objects.all()
        return render(request,'usuario/index.html',{'usuarios':usuario})

