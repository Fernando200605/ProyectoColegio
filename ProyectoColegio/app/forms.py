from dataclasses import field
from django import forms
from app.models import Curso
from app.models import Asistencia

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
        
class AsistenciaForm(forms.ModelForm):
    class Meta:
        model = Asistencia
        fields = '__all__'
        widgets = {
            'estudiante': forms.TextInput(attrs={
                'class':'form-control'
            }),
            'horaentrada':forms.TextInput(attrs={
                'class':'form-control'
            }),
            'horasalida':forms.TextInput(attrs={
                'class':'form-control'
            }),
            'estado':forms.Select(attrs={
                'class':'form-control'
            }),
            'observaciones':forms.Select(attrs={
                'class':'form-control'
            }),
            'fecha':forms.Select(attrs={
                'class':'form-control'
            })
        }
        
    # Validación personalizada para el campo capacidad
    def clean_capacidad(self):
        capacidad = self.cleaned_data.get('capacidad')
        if capacidad <= 0:
            raise forms.ValidationError("La capacidad debe ser un numero positivo.")
        return capacidad