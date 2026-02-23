from django import forms
from app.models import Curso, Usuario, Estudiante, docente, Acudiente, Administrador
from app.models import Curso
from app.models import categoria
from app.models import Elemento
from django import forms
from app.models import marca, tipoelemento, UnidadMedida, Elemento
from app.models import Asistencia
from app.models import Movimiento
from app.models import Evento
from app.models import Notificacion
from django.utils import timezone

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
            'estudiante-id': forms.Select(attrs={
                'class': 'form-control'
            }),
            
            'horaentrada': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),

            'horasalida': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),

            'estado': forms.Select(attrs={
                'class': 'form-control'
            }),

            'observaciones': forms.TextInput(attrs={ 
                'class': 'form-control'
            }),

            'fecha': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            })
        }

    def clean_observaciones(self):
        observaciones = self.cleaned_data.get('observaciones')

        if len(observaciones) > 200:
            raise forms.ValidationError("La descripción no puede superar los 200 caracteres.")

        if len(observaciones) < 10:
            raise forms.ValidationError("La descripción debe tener mínimo 10 caracteres.")

        return observaciones
    

    def clean(self):
        cleaned_data = super().clean()

        estudiante = cleaned_data.get('estudianteid')
        horaentrada = cleaned_data.get('horaentrada')
        horasalida = cleaned_data.get('horasalida')
        if estudiante:
            fecha_hoy = timezone.now().date()

            existe = Asistencia.objects.filter(
                estudianteid=estudiante,
                fecha__date=fecha_hoy
            ).exclude(pk=self.instance.pk).exists()

            if existe:
                self.add_error(
                    'estudianteid',
                    'Este estudiante ya tiene asistencia registrada hoy.'
                )

        if horaentrada and horasalida:
            if horaentrada >= horasalida:
                self.add_error(
                    'horasalida',
                    'La hora de salida no puede ser igual o menor a la hora de entrada'
                )

        return cleaned_data


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
    # Validación personalizada para el campo capacidad
