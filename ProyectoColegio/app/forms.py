from dataclasses import field
from django import forms
from app.models import Curso
from app.models import categoria
from app.models import Elemento
from django import forms
from app.models import marca, tipoelemento, UnidadMedida, Elemento

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

