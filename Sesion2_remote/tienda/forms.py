from django import forms
from django import forms
from .models import productos

class ProductoForm(forms.Form):
    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        for p in productos:
            if p['nombre'].strip().lower() == nombre.strip().lower():
                raise forms.ValidationError('Ya existe un producto con ese nombre')
        return nombre
    nombre = forms.CharField(max_length=100, label="Nombre")
    precio = forms.FloatField(
        label="Precio",
        min_value=0.01,
        error_messages={'min_value': 'El precio debe ser mayor a 0'}
    )
    stock = forms.IntegerField(
        label="Stock",
        min_value=0,
        error_messages={'min_value': 'El stock no puede ser negativo'}
    )
    categoria = forms.CharField(max_length=50, label="Categoría")