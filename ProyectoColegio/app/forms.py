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
    Administrador, Acudiente,
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
        fields = ['nombre', 'email', 'password', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
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


class TipoElementoForm(forms.ModelForm):
    class Meta:
        model = tipoelemento
        fields = '__all__'

    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre")
        patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$"
        exist = tipoelemento.objects.filter(
            nombre=nombre).exclude(pk=self.instance.pk).exists()
        if exist:
            self.fields["nombre"].widget.attrs["class"] = "form-control-invalid"
            raise forms.ValidationError(
                "Este Tipo De Elemento ya se encuentra Registrado")
        if not re.match(patron, nombre):
            raise forms.ValidationError(
                "El Nombre No es Valido (No se usan caracteres especiales ni numeros)")
        return nombre


class UnidadMedidaForm(forms.ModelForm):
    class Meta:
        model = UnidadMedida
        fields = '__all__'

    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre")
        exist = UnidadMedida.objects.filter(
            nombre=nombre).exclude(pk=self.instance.pk).exists()
        patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$"
        if exist:
            self.fields["nombre"].widget.attrs["class"] = "form-control-invalid"
            raise forms.ValidationError(
                "Esta Unidad de Medida ya se encuentra Registrado")
        if not re.match(patron, nombre):
            raise forms.ValidationError(
                "El Nombre No es Valido (No se usan caracteres especiales ni numeros)")
        if not len(nombre) <= 4 and len(nombre) >= 1:
            raise forms.ValidationError(
                "El Nombre de la Unidad debe ser una abreviacion de maximo 4 caracteres")
        return nombre


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

    def clean_nombre(self):
            nombre = self.cleaned_data['nombre']
            exist = Elemento.objects.filter(nombre=nombre).exclude(
                pk=self.instance.pk).exists()
            patron = r"^[A-Za-z 0-9 ÁÉÍÓÚáéíóúÑñ ]+$"
            if exist:
                print('aqui')
                self.fields["nombre"].widget.attrs["class"] = "form-control-invalid"
                raise forms.ValidationError(
                    "Este Elemento ya se encuentra Registrado")
            if not re.match(patron, nombre):
                raise forms.ValidationError(
                    "El Nombre No es Valido (No se usan caracteres especiales ni numeros)")
            return nombre

    def clean_stockActual(self):
            stock = self.cleaned_data.get("stockActual")
            if stock < 0:
                raise forms.ValidationError("El stock no puede ser negativo ")
            if not stock.is_integer():
                raise forms.ValidationError("El stock no puede ser decimal ")
            return stock

    def clean_stockMinimo(self):
            stock = self.cleaned_data.get("stockMinimo")
            if stock < 0:
                raise forms.ValidationError("El stock no puede ser negativo ")
            if not stock.is_integer():
                raise forms.ValidationError("El stock no puede ser decimal ")
            return stock
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

    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo')

        if Evento.objects.filter(titulo__iexact=titulo).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Ya existe un evento con este título.")

        return titulo

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')

        if not descripcion:
            raise forms.ValidationError("La descripción es obligatoria.")

        if len(descripcion) > 200:
            raise forms.ValidationError("La descripción no puede superar los 200 caracteres.")

        if len(descripcion) < 10:
            raise forms.ValidationError("La descripción debe tener mínimo 10 caracteres.")

        return descripcion

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')

        if fecha_inicio and fecha_fin:
            if fecha_inicio >= fecha_fin:
                self.add_error('fecha_fin', "La fecha de fin debe ser mayor que la fecha de inicio.")

        return cleaned_data
    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo')

        # Validación 1: No permitir que sea solo números
        if titulo.isdigit():
            raise forms.ValidationError("El título no puede contener solo números.")

        # Validación 2: No permitir caracteres especiales
        if not re.match(r'^[a-zA-ZÁÉÍÓÚáéíóúÑñ0-9 ]+$', titulo):
            raise forms.ValidationError("El título no puede contener caracteres especiales.")

        return titulo
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

# ELEMENTO


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
