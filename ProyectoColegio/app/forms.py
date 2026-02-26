import re
from django import forms
from app.models import Curso, Usuario, Estudiante, docente, Acudiente, Administrador


# ── Helper de validación 

def solo_letras(value, campo="Este campo"):
    """Solo letras (incluye tildes, ñ y espacios). Sin números ni especiales."""
    value = value.strip()
    if not value:
        raise forms.ValidationError(f"{campo} es obligatorio.")
    if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$", value):
        raise forms.ValidationError(
            f"{campo} solo puede contener letras y espacios, sin números ni caracteres especiales."
        )
    return value


# ── Formulario de Cursos 

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = '__all__'
        widgets = {
            'nom':       forms.TextInput(attrs={'class': 'form-control'}),
            'jornada':   forms.TextInput(attrs={'class': 'form-control'}),
            'codigo':    forms.TextInput(attrs={'class': 'form-control'}),
            'capacidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'docenteid': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_nom(self):
        return solo_letras(self.cleaned_data.get('nom', ''), "El nombre del curso")

    def clean_jornada(self):
        return solo_letras(self.cleaned_data.get('jornada', ''), "La jornada")

    def clean_capacidad(self):
        capacidad = self.cleaned_data.get('capacidad')
        if capacidad <= 0:
            raise forms.ValidationError("La capacidad debe ser un número positivo.")
        return capacidad


# ── Formulario para Crear Usuario ────────────────────────────────────────────

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'email', 'contraseña', 'estado']
        widgets = {
            'nombre':     forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Nombre completo'
            }),
            'email':      forms.EmailInput(attrs={
                'class': 'form-control', 'placeholder': 'correo@ejemplo.com'
            }),
            'contraseña': forms.PasswordInput(attrs={
                'class': 'form-control', 'placeholder': 'Contraseña',
                'id': 'id_contraseña'
            }),
            'estado':     forms.Select(attrs={'class': 'form-control'}),
        }

    # Nombre: solo letras
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        if not nombre:
            raise forms.ValidationError("El nombre es obligatorio.")
        return solo_letras(nombre, "El nombre")

    #  Email 
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            return email

        email = email.lower()

        if Usuario.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            self.fields['email'].widget.attrs['class'] = 'form-control is-invalid'
            raise forms.ValidationError(
                "Este correo ya se encuentra registrado. Intenta con uno diferente."
            )

        dominios_permitidos = ['gmail.com', 'hotmail.com', 'outlook.com', 'yahoo.com']
        partes = email.split('@')
        if len(partes) > 1 and partes[1] not in dominios_permitidos:
            self.fields['email'].widget.attrs['class'] = 'form-control is-invalid'
            raise forms.ValidationError(
                f"Solo se permiten correos de: {', '.join(dominios_permitidos)}"
            )

        return email

    #  Contraseña 
    def clean_contraseña(self):
        password = self.cleaned_data.get('contraseña')
        if not password:
            return password

        errores = []
        if len(password) < 8:
            errores.append("al menos 8 caracteres")
        if not any(c.isupper() for c in password):
            errores.append("una mayúscula")
        if not any(c.isdigit() for c in password):
            errores.append("un número")

        if errores:
            self.fields['contraseña'].widget.attrs['class'] = 'form-control is-invalid'
            raise forms.ValidationError(f"Falta: {', '.join(errores)}.")

        return password

    #  Confirmar contraseña 
    def clean(self):
        cleaned_data = super().clean()
        password         = cleaned_data.get('contraseña')
        confirm_password = self.data.get('confirmar_contraseña')

        if password and confirm_password and password != confirm_password:
            self.fields['contraseña'].widget.attrs['class'] = 'form-control is-invalid'
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data


#  Formulario para Editar Usuario 

class UsuarioUpdateForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'email', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'email':  forms.EmailInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        return solo_letras(nombre, "El nombre")


# Formularios de Roles 

class AdministradorForm(forms.ModelForm):
    class Meta:
        model = Administrador
        fields = ['cargo']
        widgets = {
            'cargo': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Cargo'
            })
        }

    def clean_cargo(self):
        return solo_letras(
            self.cleaned_data.get('cargo', ''), "El cargo"
        )


class DocenteForm(forms.ModelForm):
    class Meta:
        model = docente
        fields = ['especialidad']
        widgets = {
            'especialidad': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

    def clean_especialidad(self):
        
        return solo_letras(
            self.cleaned_data.get('especialidad', ''), "La especialidad"
        )


class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['codigo', 'fechaNacimiento', 'estadoMatricula', 'fechaIngreso', 'cursoId']
        widgets = {
            'codigo':          forms.TextInput(attrs={'class': 'form-control'}),
            'fechaNacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estadoMatricula': forms.Select(attrs={'class': 'form-control'}),
            'fechaIngreso':    forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'cursoId':         forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo', '')
        if not re.match(r'^\d+$', codigo):
            raise forms.ValidationError("El código solo puede contener números.")
        return codigo


class AcudienteForm(forms.ModelForm):
    class Meta:
        model = Acudiente
        fields = ['telefono', 'direccion']
        widgets = {
            'telefono':  forms.TextInput(attrs={'class': 'form-control', 'maxlength': '10'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono', '')
        if not re.match(r'^\d{7,10}$', telefono):
            raise forms.ValidationError(
                "El teléfono debe contener solo dígitos (7 a 10 cifras)."
            )
        return telefono

    def clean_direccion(self):
        # Sin restricciones: acepta letras, números y caracteres especiales
        return self.cleaned_data.get('direccion', '')