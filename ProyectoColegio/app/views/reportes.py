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
    
    
# ====== VISTAS PARA EXPORTAR REPORTES MOVIMIENTOS ======

class ExportarMovimientosPDF(DjangoView):
    """
    VISTA PARA EXPORTAR Movimientos A PDF
    Obtiene todas los movimientos y los exporta en formato PDF
    """
    
    def get(self, request):
        # Obtener todas las categorias 
        movimiento = Movimiento.objects.all()
        
        # Definir las columnas que se muestran en el reporte
        columnas = ["id", "fecha", 'cantidad',"elementoid","usuarioid","cursoid"]
        
        # Preparar los datos en formato de tuplas
        datos = [
            (mo.id,mo.fecha, mo.cantidad,mo.elementoid,mo.usuarioid,mo.cursoid)
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
        columnas = ["id",'fecha', 'cantidad',"elementoid","usuarioid","cursoid"]
        
        # Preparar los datos en  tuplas
        datos = [
            (mo.id,mo.fecha, mo.cantidad,mo.elementoid,mo.usuarioid,mo.cursoid)
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
    