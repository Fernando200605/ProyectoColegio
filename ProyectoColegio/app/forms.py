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
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email: 
            return email
        
        email = email.lower()

        existe = Usuario.objects.filter(email=email).exclude(pk=self.instance.pk).exists()
        
        if existe:
            self.fields['email'].widget.attrs['class'] = 'form-control is-invalid'
            raise forms.ValidationError("Este correo ya se encuentra registrado. Intenta con uno diferente.")

        dominios_permitidos = ['gmail.com', 'hotmail.com', 'outlook.com', 'yahoo.com']
        partes = email.split('@')
        
        if len(partes) > 1 and partes[1] not in dominios_permitidos:
            self.fields['email'].widget.attrs['class'] = 'form-control is-invalid'
            raise forms.ValidationError(f"Solo se permiten correos de: {', '.join(dominios_permitidos)}")
        
        return email
        
    def clean_contraseña(self):
            password = self.cleaned_data.get('contraseña')
            if not password:
                return password

            errores = []
            if len(password) < 8:
                errores.append("al menos 8 caracteres")
            if not any(char.isupper() for char in password):
                errores.append("una mayúscula")
            if not any(char.isdigit() for char in password):
                errores.append("un número")
            
            if errores:
                self.fields['contraseña'].widget.attrs['class'] = 'form-control is-invalid'
                raise forms.ValidationError(f"Falta: {', '.join(errores)}.")

            return password
    #Confirmar contraseña
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('contraseña')
        confirm_password = self.data.get('confirmar_contraseña')

        if password and confirm_password and password != confirm_password:
            self.fields['contraseña'].widget.attrs['class'] = 'form-control is-invalid'
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data

# Formulario para Editar Usuario 
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