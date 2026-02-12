from dataclasses import field
from django import forms
from app.models import Curso
from app.models import Movimiento
from app.models import Evento
from app.models import Notificacion

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
    # Validación personalizada para el campo capacidad
    def clean_capacidad(self):
        capacidad = self.cleaned_data.get('capacidad')
        if capacidad <= 0:
            raise forms.ValidationError("La capacidad debe ser un numero positivo.")
        return capacidad
    
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
    def clean_capacidad(self):
        capacidad = self.cleaned_data.get('capacidad')
        if capacidad <= 0:
            raise forms.ValidationError("La capacidad debe ser un numero positivo.")
        return capacidad
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
    def clean_capacidad(self):
        capacidad = self.cleaned_data.get('capacidad')
        if capacidad <= 0:
            raise forms.ValidationError("La capacidad debe ser un numero positivo.")
        return capacidad