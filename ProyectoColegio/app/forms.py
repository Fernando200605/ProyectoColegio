from django import forms
from app.models import (
    Curso,
    categoria,
    Elemento,
    marca,
    tipoelemento,
    UnidadMedida,
    Movimiento,
    Eventos,
)
import re

# CURSO
class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = '__all__'
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'jornada': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'capacidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'docenteid': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_capacidad(self):
        capacidad = self.cleaned_data.get('capacidad')

        if capacidad is None or capacidad <= 0:
            raise forms.ValidationError(
                "La capacidad debe ser un número positivo."
            )

        return capacidad

# MARCA

class MarcaForm(forms.ModelForm):
    class Meta:
        model = marca
        fields = '__all__'

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        nombre = re.sub(r'\s+', ' ', nombre)

        if len(nombre) < 3:
            raise forms.ValidationError(
                "El nombre debe tener al menos 3 caracteres."
            )

        patron = r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$'
        if not re.match(patron, nombre):
            raise forms.ValidationError(
                "El nombre solo puede contener letras y espacios."
            )

        if marca.objects.filter(
            nombre__iexact=nombre
        ).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(
                "Ya existe una marca con este nombre."
            )

        return nombre

# CATEGORIA

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = categoria
        fields = ['nombre']

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        nombre = re.sub(r'\s+', ' ', nombre)

        if len(nombre) < 3:
            raise forms.ValidationError(
                "El nombre debe tener al menos 3 caracteres."
            )

        patron = r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$'
        if not re.match(patron, nombre):
            raise forms.ValidationError(
                "El nombre solo puede contener letras y espacios."
            )

        if categoria.objects.filter(
            nombre__iexact=nombre
        ).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(
                "Ya existe una categoría con este nombre."
            )

        return nombre

# TIPO ELEMENTO


class TipoElementoForm(forms.ModelForm):
    class Meta:
        model = tipoelemento
        fields = '__all__'

# UNIDAD DE MEDIDA

class UnidadMedidaForm(forms.ModelForm):
    class Meta:
        model = UnidadMedida
        fields = '__all__'


# ELEMENTO

class ElementoForm(forms.ModelForm):
    class Meta:
        model = Elemento
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'stockActual': forms.NumberInput(attrs={'class': 'form-control'}),
            'stockMinimo': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipoElementoId': forms.Select(attrs={'class': 'form-control'}),
            'categoriaId': forms.Select(attrs={'class': 'form-control'}),
            'marcaId': forms.Select(attrs={'class': 'form-control'}),
            'unidadMedidaId': forms.Select(attrs={'class': 'form-control'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
        }

    # 🔹 Validación individual de ubicación
    def clean_ubicacion(self):
        ubicacion = self.cleaned_data.get('ubicacion', '').strip()
        ubicacion = re.sub(r'\s+', ' ', ubicacion)

        if len(ubicacion) < 3:
            raise forms.ValidationError(
                "La ubicación debe tener al menos 3 caracteres."
            )

        patron = r'^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑüÜ\s\-]+$'
        if not re.match(patron, ubicacion):
            raise forms.ValidationError(
                "La ubicación solo puede contener letras, números y guiones."
            )

        return ubicacion

    # 🔹 Validación cruzada profesional
    def clean(self):
        cleaned_data = super().clean()

        stock_actual = cleaned_data.get('stockActual')
        stock_minimo = cleaned_data.get('stockMinimo')

        if stock_actual is not None and stock_actual < 0:
            self.add_error(
                'stockActual',
                "El stock actual no puede ser negativo."
            )

        if stock_minimo is not None and stock_minimo < 0:
            self.add_error(
                'stockMinimo',
                "El stock mínimo no puede ser negativo."
            )

        if (
            stock_actual is not None and
            stock_minimo is not None and
            stock_minimo > stock_actual
        ):
            self.add_error(
                'stockMinimo',
                "El stock mínimo no puede ser mayor que el stock actual."
            )

        return cleaned_data


# MOVIMIENTO

class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = '__all__'

# EVENTO

class EventoForm(forms.ModelForm):
    class Meta:
        model = Eventos
        fields = '__all__'
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'fecha_fin': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        inicio = cleaned_data.get('fecha_inicio')
        fin = cleaned_data.get('fecha_fin')

        if inicio and fin and fin <= inicio:
            self.add_error(
                'fecha_fin',
                "La fecha de fin debe ser posterior a la fecha de inicio."
            )

        return cleaned_data