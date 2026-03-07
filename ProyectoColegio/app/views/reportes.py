from django.shortcuts import render
from django.views.generic import View
from django.views import View as DjangoView
from django.http import HttpResponse
from app.models import *
from app.utils import exportar_pdf, exportar_excel
from datetime import datetime

# ====== VISTAS PARA EXPORTAR REPORTES ======

class ExportarCategoriasPDF(DjangoView):
    """
    VISTA PARA EXPORTAR CATEGORIAS A PDF
    Obtiene todas las categorías y las exporta en formato PDF
    """
    
    def get(self, request):
        # Obtener todas las categorias 
        usuario = Usuario.objects.all()
        
        # Definir las columnas que se muestran en el reporte
        columnas = ['ID', 'Nombre', 'email']
        
        # Preparar los datos en formato de tuplas
        datos = [
            (us.id, us.nombre, us.email)
            for us in usuario
        ]
        
        # Generar nombre del archivo con timestamp
        nombre_archivo = f'Reporte_Categorias_{datetime.now().strftime("%d_%m_%Y")}'
        
        # Llamar funcion de exportacion a PDF
        return exportar_pdf(
            request,
            titulo='REPORTE DE CATEGORIAS',
            columnas=columnas,
            datos=datos,
            nombre_archivo=nombre_archivo,
            
        )


class ExportarCategoriasExcel(DjangoView):
    """
    VISTA PARA EXPORTAR CATEGORIAS A EXCEL
    Obtiene todas las categorias y las exporta en formato Excel
    """
    
    def get(self, request):
        # Obtener todas las categorias 
        usuario = Usuario.objects.all()
        
        # Definir las columnas que se mostraran en el reporte
        columnas = ['ID', 'Nombre', 'Descripcion']
        
        # Preparar los datos en  tuplas
        datos = [
            (cat.id, cat.nombre, cat.descripcion)
            for cat in usuario
        ]
        
        # Generar nombre del archivo con timestamp
        nombre_archivo = f'Reporte_Categorias_{datetime.now().strftime("%d_%m_%Y")}'
        
        # Llamar funcion de exportacion a Excel
        return exportar_excel(
            titulo='REPORTE DE CATEGORIAS',
            columnas=columnas,
            datos=datos,
            nombre_archivo=nombre_archivo
        )
class ExportarCursoExcel(DjangoView):
    def get(self, request):
        # 1. Capturamos el ID que viene del selector del HTML
        curso_id = request.GET.get('curso_id')
        
        # 2. Si hay un ID, filtramos. Si no, traemos todos.
        if curso_id:
            cursos = Curso.objects.filter(id=curso_id)
            titulo_reporte = f'REPORTE DEL CURSO #{curso_id}'
        else:
            cursos = Curso.objects.all()
            titulo_reporte = 'REPORTE GENERAL DE CURSOS'
        
        columnas = ['ID', 'Grado', 'Código', 'Capacidad']
        
        # Usamos la variable 'cursos' que ya está filtrada arriba
        datos = [
            (c.id, c.grado, c.codigo, c.capacidad) 
            for c in cursos
        ]
        
        nombre_archivo = f'Reporte_Cursos_{datetime.now().strftime("%d_%m_%Y")}'
        
        return exportar_excel(
            titulo=titulo_reporte,
            columnas=columnas,
            datos=datos,
            nombre_archivo=nombre_archivo
        )

class ExportarCursoPDF(DjangoView):
    def get(self, request):
        # 1. Capturamos el ID que viene del selector del HTML
        curso_id = request.GET.get('curso_id')
        
        # 2. Si hay un ID, filtramos. Si no, traemos todos.
        if curso_id:
            cursos = Curso.objects.filter(id=curso_id)
            # Intentamos obtener el nombre del grado para un título más bonito
            curso_obj = cursos.first()
            grado_nombre = curso_obj.get_grado_display() if curso_obj else curso_id
            titulo_reporte = f'REPORTE DEL CURSO: {grado_nombre}'
        else:
            cursos = Curso.objects.all()
            titulo_reporte = 'REPORTE GENERAL DE CURSOS'
        
        columnas = ['ID', 'Grado', 'Código', 'Capacidad']
        
        # 3. Preparamos los datos usando la variable 'cursos' (ya filtrada)
        datos = [
            (c.id, c.grado, c.codigo, c.capacidad) 
            for c in cursos
        ]
        
        nombre_archivo = f'Reporte_Cursos_{datetime.now().strftime("%d_%m_%Y")}'
        
        # 4. Retornamos la función que genera el PDF
        return exportar_pdf(
            request,
            titulo=titulo_reporte,
            columnas=columnas,
            datos=datos,
            nombre_archivo=nombre_archivo
        )