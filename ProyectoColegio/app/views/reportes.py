from django.shortcuts import render, redirect
from django.views.generic import View
from django.views import View as DjangoView
from django.http import HttpResponse
from app.models import *
from django.db.models import Q
from app.utils import exportar_pdf, exportar_excel
from datetime import datetime
from django.contrib import messages
# ====== VISTAS PARA EXPORTAR REPORTES ======


class ExportarUsuarioPDF(DjangoView):

    def get(self, request):
        print("Aqui")

        usuarios = Usuario.objects.all()

        buscar = request.GET.get('buscar', '').strip()
        rol = request.GET.get('rol', '').strip()
        estado = request.GET.get('estado', '').strip()

        # ===== BUSQUEDA =====
        if buscar:
            usuarios = usuarios.filter(
                Q(nombre__icontains=buscar) |
                Q(email__icontains=buscar)
            )

        # ===== ESTADO =====
        if estado in ['0', '1']:
            usuarios = usuarios.filter(estado=estado)

        # ===== ROL =====
        if rol == "administrador":
            usuarios = usuarios.filter(administrador__isnull=False)

        elif rol == "docente":
            usuarios = usuarios.filter(docente__isnull=False)

        elif rol == "estudiante":
            usuarios = usuarios.filter(estudiante__isnull=False)

        # ===== VALIDAR RESULTADOS =====
        if not usuarios.exists():
            messages.warning(request, "No existen usuarios con ese filtro")
            return redirect('app:index_usuario')

        columnas = ['ID', 'Nombre', 'Email', 'Rol', 'Estado']

        datos = [
            (
                us.id,
                us.nombre,
                us.email,
                us.get_rol(),
                "Activo" if us.estado else "Inactivo"
            )
            for us in usuarios
        ]

        nombre_archivo = f'Reporte_Usuarios_{datetime.now().strftime("%d_%m_%Y")}'

        return exportar_pdf(
            request,
            titulo='REPORTE DE USUARIOS',
            columnas=columnas,
            datos=datos,
            nombre_archivo=nombre_archivo
        )


class ExportarUsuarioExcel(DjangoView):
    """
    VISTA PARA EXPORTAR CATEGORIAS A EXCEL
    Obtiene todas las categorias y las exporta en formato Excel
    """

    def get(self, request):
        print("Aqui")

        usuarios = Usuario.objects.all()

        buscar = request.GET.get('buscar', '').strip()
        rol = request.GET.get('rol', '').strip()
        estado = request.GET.get('estado', '').strip()

        # ===== BUSQUEDA =====
        if buscar:
            usuarios = usuarios.filter(
                Q(nombre__icontains=buscar) |
                Q(email__icontains=buscar)
            )

        # ===== ESTADO =====
        if estado in ['0', '1']:
            usuarios = usuarios.filter(estado=estado)

        # ===== ROL =====
        if rol == "administrador":
            usuarios = usuarios.filter(administrador__isnull=False)

        elif rol == "docente":
            usuarios = usuarios.filter(docente__isnull=False)

        elif rol == "estudiante":
            usuarios = usuarios.filter(estudiante__isnull=False)

        # ===== VALIDAR RESULTADOS =====
        if not usuarios.exists():
            messages.warning(request, "No existen usuarios con ese filtro")
            return redirect('app:index_usuario')

        columnas = ['ID', 'Nombre', 'Email', 'Rol', 'Estado']

        datos = [
            (
                us.id,
                us.nombre,
                us.email,
                us.get_rol(),
                "Activo" if us.estado else "Inactivo"
            )
            for us in usuarios
        ]

        nombre_archivo = f'Reporte_Usuarios_{datetime.now().strftime("%d_%m_%Y")}'

        # Llamar funcion de exportacion a Excel
        return exportar_excel(
            titulo='REPORTE DE CATEGORIAS',
            columnas=columnas,
            datos=datos,
            nombre_archivo=nombre_archivo
        )
