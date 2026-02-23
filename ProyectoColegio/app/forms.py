from django import forms
from app.models import (
    Curso,
    categoria,
    Elemento,
    marca,
    tipoelemento,
    UnidadMedida,
    Movimiento,
    Evento,
    Asistencia,
    Usuario,
    Administrador,Acudiente,
    Estudiante,
    docente,
    Notificacion
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
            'docenteid': forms.Select(attrs={'class': 'form-control'})
        }
        def clean_capacidad(self):
            capacidad = self.cleaned_data.get('capacidad')
            if capacidad <= 0:
                raise forms.ValidationError(
                    "La capacidad debe ser un número positivo.")
            return capacidad


class AsistenciaForm(forms.ModelForm):
    class Meta:
        model = Asistencia
        fields = '__all__'
        widgets = {
            'estudiante': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'horaentrada': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'horasalida': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-control'
            }),
            'observaciones': forms.Select(attrs={
                'class': 'form-control'
            }),
            'fecha': forms.Select(attrs={
                'class': 'form-control'
            })
        }

    # Validación personalizada para el campo capacidad


# Formulario para Crear Usuario (Con Contraseña)
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'email', 'contraseña', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
            'contraseña': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }

# Formulario para Editar Usuario (Sin Contraseña)


class UsuarioUpdateForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'email', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }

# Formularios de Roles


class AdministradorForm(forms.ModelForm):
    class Meta:
        model = Administrador
        fields = ['cargo']
        widgets = {'cargo': forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Cargo'})}


class DocenteForm(forms.ModelForm):
    class Meta:
        model = docente
        fields = ['especialidad']
        widgets = {'especialidad': forms.Textarea(
            attrs={'class': 'form-control', 'rows': 3})}


class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['codigo', 'fechaNacimiento',
                  'estadoMatricula', 'fechaIngreso', 'cursoId']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'fechaNacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estadoMatricula': forms.Select(attrs={'class': 'form-control'}),
            'fechaIngreso': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'cursoId': forms.Select(attrs={'class': 'form-control'})
        }


class AcudienteForm(forms.ModelForm):
    class Meta:
        model = Acudiente
        fields = ['telefono', 'direccion']
        widgets = {
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '10'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
        }


class marcaForm(forms.ModelForm):
    class Meta:
        model = marca
        fields = '__all__'


class TipoElementoForm(forms.ModelForm):
    class Meta:
        model = tipoelemento
        fields = '__all__'


class UnidadMedidaForm(forms.ModelForm):
    class Meta:
        model = UnidadMedida
        fields = '__all__'


class ElementoForm(forms.ModelForm):
    class Meta:
        model = Elemento
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'unidad_medida': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = categoria
        fields = ['nombre']
    
class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = '__all__'
        widgets = {
            'nom': forms.TextInput(attrs={
                'class':'form-control'
            }),
            'jornada':forms.TextInput(attrs={
                'class':'form-control'
            }),
            'codigo':forms.TextInput(attrs={
                'class':'form-control'
            }),
            'capacidad':forms.NumberInput(attrs={
                'class':'form-control'
            }),
            'docenteid':forms.Select(attrs={
                'class':'form-control'
            })
        }
    
class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = '__all__'
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'fecha_fin': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    # Validación personalizada para el campo capacidad

class NotificacionForm(forms.ModelForm):
    class Meta:
        model = Notificacion
        fields = '__all__'
        widgets = {
            'nom': forms.TextInput(attrs={
                'class':'form-control'
            }),
            'jornada':forms.TextInput(attrs={
                'class':'form-control'
            }),
            'codigo':forms.TextInput(attrs={
                'class':'form-control'
            }),
            'capacidad':forms.NumberInput(attrs={
                'class':'form-control'
            }),
            'docenteid':forms.Select(attrs={
                'class':'form-control'
            })
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
        model = Evento
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
