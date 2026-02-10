from django import forms
from app.models import Curso, Usuario, Estudiante, docente, Acudiente, Administrador

# Formulario para Cursos
class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = '__all__'
        widgets = {
            'nom': forms.TextInput(attrs={'class':'form-control'}),
            'jornada':forms.TextInput(attrs={'class':'form-control'}),
            'codigo':forms.TextInput(attrs={'class':'form-control'}),
            'capacidad':forms.NumberInput(attrs={'class':'form-control'}),
            'docenteid':forms.Select(attrs={'class':'form-control'})
        }
    
    def clean_capacidad(self):
        capacidad = self.cleaned_data.get('capacidad')
        if capacidad <= 0:
            raise forms.ValidationError("La capacidad debe ser un número positivo.")
        return capacidad

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
        widgets = {'cargo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cargo'})}

class DocenteForm(forms.ModelForm):
    class Meta:
        model = docente
        fields = ['especialidad']
        widgets = {'especialidad': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})}

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['codigo', 'fechaNacimiento', 'estadoMatricula', 'fechaIngreso', 'cursoId']
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