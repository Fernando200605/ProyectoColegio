from dataclasses import field
from django import forms
from app.models import Curso , Usuario

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
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
    def clean_capacidad(self):
        capacidad = self.cleaned_data.get('capacidad')
        if capacidad <= 0:
            raise forms.ValidationError("La capacidad debe ser un numero positivo.")
        return capacidad
    
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre','email','contraseña','estado']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class':'form-control'
            }),
            'email':forms.EmailInput(attrs={
                'class':'form-control'
            }),
            'contraseña':forms.PasswordInput(attrs={
                'class':'form-control'
            }),
            'estado':forms.Select(attrs={
                'class':'form-control'
            }),
        }