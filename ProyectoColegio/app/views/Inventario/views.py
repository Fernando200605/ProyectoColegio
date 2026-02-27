from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView , View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from app.models import *
from app.forms import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import connection
from django.db.models import Q, F

# ===============================
# LISTAR INVENTARIO (Función simple)
# ===============================

def listar_inventario(request):
    elementos = Elemento.objects.all()
    return render(request, 'inventario/index.html', {'elementos': elementos})

# ===============================
# LIST VIEW - INVENTARIO (igual estilo a CursoListView)
# ===============================

class InventarioListView(ListView):
    model = Elemento
    template_name = 'inventario/index.html'
    context_object_name = 'elementos'
    paginate_by = 10  # Paginación como buena práctica

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Elemento.objects.select_related(
            "tipoElementoId", "categoriaId", "marcaId", "unidadMedidaId"
        ).all()

        # 🔍 Búsqueda general
        buscar = self.request.GET.get("buscar")
        if buscar:
            queryset = queryset.filter(
                Q(nombre__icontains=buscar) |
                Q(descripcion__icontains=buscar) |
                Q(ubicacion__icontains=buscar)
            )

        # ⚠️ Filtro de stock bajo
        bajo_stock = self.request.GET.get("bajo_stock")
        if bajo_stock == "1":
            queryset = queryset.filter(stockActual__lte=F("stockMinimo"))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Inventario General'
        context['subtitulo'] = 'Gestión de elementos del colegio'
        context['crear_url'] = reverse_lazy('app:crear_elemento')
        context['icon_primary'] = "fa-arrow-up"
        context['icon_secodary'] = "fa-arrow-down"
        # Contadores útiles
        context['total_elementos'] = Elemento.objects.count()
        context['stock_bajo'] = Elemento.objects.filter(
            stockActual__lte=F("stockMinimo")
        ).count()

        return context

# ===============================
# CREATE VIEW - CREAR ELEMENTO
# ===============================

class ElementoCreateView(CreateView):
    model = Elemento
    form_class = ElementoForm
    template_name = 'inventario/crear.html'
    success_url = reverse_lazy('app:index_inventario')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar Elemento"
        context['listar_url'] = reverse_lazy('app:index_inventario')
        context['btn_name'] = "Guardar"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Elemento registrado correctamente")
        return super().form_valid(form)

# ===============================
# UPDATE VIEW - ACTUALIZAR ELEMENTO
# ===============================

class ElementoUpdateView(UpdateView):
    model = Elemento
    form_class = ElementoForm
    template_name = 'inventario/crear.html'
    success_url = reverse_lazy('app:index_inventario')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Actualizar Elemento"
        context['listar_url'] = reverse_lazy('app:index_inventario')
        context['btn_name'] = "Actualizar"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Elemento actualizado correctamente")
        return super().form_valid(form)

# ===============================
# DELETE VIEW - ELIMINAR ELEMENTO
# ===============================

class ElementoDeleteView(DeleteView):
    model = Elemento
    template_name = 'inventario/eliminar.html'
    success_url = reverse_lazy('app:index_inventario')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Eliminar Elemento"
        context['listar_url'] = reverse_lazy('app:index_inventario')
        return context

    def form_valid(self, form):
        messages.success(self.request, "Elemento eliminado correctamente")
        return super().form_valid(form)

# ===============================
# LIMPIAR INVENTARIO (BORRAR TODO Y REINICIAR ID)
# ===============================

class InventarioCleanView(View):
    def post(self, request, *args, **kwargs):
        Elemento.objects.all().delete()

        with connection.cursor() as cursor:
            nombre_tabla = Elemento._meta.db_table
            cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{nombre_tabla}';")

        messages.success(self.request, "Todo el inventario ha sido eliminado y el ID reiniciado.")
        return redirect(reverse_lazy('app:index_inventario'))
