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


class ExportarAsistenciaPDF(DjangoView):
    """
    VISTA PARA EXPORTAR CATEGORIAS A PDF
    Obtiene todas las categorías y las exporta en formato PDF
    """

    def get(self, request):
        # Obtener todas las categorias
        asistencia = Asistencia.objects.all()

        # Definir las columnas que se muestran en el reporte
        columnas = ['ID', 'NOMBRE DEL ESTUDIANTE', 'FECHA', 'OBSERVACIONES']

        # Preparar los datos en formato de tuplas
        datos = [
            (asi.id, asi.estudianteid, asi.fecha, asi.observaciones)
            for asi in asistencia
        ]

        # Generar nombre del archivo con timestamp
        nombre_archivo = f'Reporte_Asistencias_{datetime.now().strftime("%d_%m_%Y")}'

        # Llamar funcion de exportacion a PDF
        return exportar_pdf(
            request,
            titulo='REPORTE DE ASISTENCIAS',
            columnas=columnas,
            datos=datos,
            nombre_archivo=nombre_archivo,

        )


class ExportarAsistenciaExcel(DjangoView):
    """
    VISTA PARA EXPORTAR CATEGORIAS A EXCEL
    Obtiene todas las categorias y las exporta en formato Excel
    """

    def get(self, request):
        # Obtener todas las categorias
        asistencia = Asistencia.objects.all()

        # Definir las columnas que se mostraran en el reporte
        columnas = ['ID', 'NOMBRE DEL ESTUDIANTE', 'FECHA', 'OBSERVACIONES']

        # Preparar los datos en  tuplas
        datos = [
            (asi.id, asi.estudianteid, asi.fecha, asi.observaciones)
            for asi in asistencia
        ]

        # Generar nombre del archivo con timestamp
        nombre_archivo = f'Reporte_Asistencias_{datetime.now().strftime("%d_%m_%Y")}'

        # Llamar funcion de exportacion a Excel
        return exportar_excel(
            titulo='REPORTE DE ASISTENCIA',
            columnas=columnas,
            datos=datos,
            nombre_archivo=nombre_archivo
        )


class ExportarEventosPDF(DjangoView):
    """
    VISTA PARA EXPORTAR CATEGORIAS A PDF
    Obtiene todas las categorías y las exporta en formato PDF
    """

    def get(self, request):
        # Obtener todas las categorias
        evento = Evento.objects.all()

        # Definir las columnas que se muestran en el reporte
        columnas = ['ID', 'TITULO', 'DESCRIPCION']

        # Preparar los datos en formato de tuplas
        datos = [
            (us.id, us.titulo, us.descripcion)
            for us in evento
        ]

        # Generar nombre del archivo con timestamp
        nombre_archivo = f'Reporte_Eventos_{datetime.now().strftime("%d_%m_%Y")}'

        # Llamar funcion de exportacion a PDF
        return exportar_pdf(
            request,
            titulo='REPORTE DE EVENTOS',
            columnas=columnas,
            datos=datos,
            nombre_archivo=nombre_archivo,

        )


class ExportarEventosExcel(DjangoView):

    def get(self, request):
        # Obtener todas las categorias
        evento = Evento.objects.all()

        # Definir las columnas que se muestran en el reporte
        columnas = ['ID', 'TITULO', 'DESCRIPCION']

        # Preparar los datos en formato de tuplas
        datos = [
            (us.id, us.titulo, us.descripcion)
            for us in evento
        ]

        # Generar nombre del archivo con timestamp
        nombre_archivo = f'Reporte_Eventos_{datetime.now().strftime("%d_%m_%Y")}'

        # Llamar funcion de exportacion a PDF
        return exportar_excel(
            titulo='REPORTE DE EVENTOS',
            columnas=columnas,
            datos=datos,
            nombre_archivo=nombre_archivo,

        )


class ExportarMovimientosPDF(DjangoView):
    """
    VISTA PARA EXPORTAR Movimientos A PDF
    Obtiene todas los movimientos y los exporta en formato PDF
    """

    def get(self, request):
        # Obtener todas las categorias
        movimiento = Movimiento.objects.all()

        # Definir las columnas que se muestran en el reporte
        columnas = ["id", "fecha", 'cantidad',
                    "elementoid", "usuarioid", "cursoid"]

        # Preparar los datos en formato de tuplas
        datos = [
            (mo.id, mo.fecha, mo.cantidad, mo.elementoid, mo.usuarioid, mo.cursoid)
            for mo in movimiento
        ]

        # Generar nombre del archivo con timestamp
        nombre_archivo = f'Reporte_movimientos_{datetime.now().strftime("%d_%m_%Y")}'

        # Llamar funcion de exportacion a PDF
        return exportar_pdf(
            request,
            titulo='REPORTE DE MOVIMIENTOS',
            columnas=columnas,
            datos=datos,
            nombre_archivo=nombre_archivo,

        )


class ExportarMovimientosExcel(DjangoView):
    """
    VISTA PARA EXPORTAR MOVIMIENTOS A EXCEL
    Obtiene todos los movimientos y los exporta en formato Excel
    """

    def get(self, request):
        # Obtener todas las categorias
        movimiento = Movimiento.objects.all()

        # Definir las columnas que se mostraran en el reporte
        columnas = ["id", 'fecha', 'cantidad',
                    "elementoid", "usuarioid", "cursoid"]

        # Preparar los datos en  tuplas
        datos = [
            (mo.id, mo.fecha, mo.cantidad, mo.elementoid, mo.usuarioid, mo.cursoid)
            for mo in movimiento
        ]

        # Generar nombre del archivo con timestamp
        nombre_archivo = f'Reporte_movimientos_{datetime.now().strftime("%d_%m_%Y")}'

        # Llamar funcion de exportacion a Excel
        return exportar_excel(
            titulo='REPORTE DE MOVIMIENTOS',
            columnas=columnas,
            datos=datos,
            nombre_archivo=nombre_archivo
        )
