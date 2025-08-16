# produccion/forms.py
from django import forms
from .models import OrdenProduccion, RequisicionEncabezado, ControlProceso, ReporteDiarioProductoTerminado , NotaIngresoProductoTerminado

class OrdenProduccionForm(forms.ModelForm):
    class Meta:
        model = OrdenProduccion
        fields = '__all__'
        widgets = {
            'numero_orden': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'producto_a_elaborar': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad_a_producir': forms.NumberInput(attrs={'class': 'form-control'}),
            'cantidad_hojas_por_ejemplar': forms.NumberInput(attrs={'class': 'form-control'}),
            'tiraje_total': forms.NumberInput(attrs={'class': 'form-control'}),
            'numero_de_resmas': forms.TextInput(attrs={'class': 'form-control'}),
            'medida_de_corte': forms.TextInput(attrs={'class': 'form-control'}),
            'tamano': forms.TextInput(attrs={'class': 'form-control'}),
            'papel': forms.TextInput(attrs={'class': 'form-control'}),
            'base': forms.TextInput(attrs={'class': 'form-control'}),
            'total_planchas': forms.NumberInput(attrs={'class': 'form-control'}),
            'numero_de_pliegos': forms.NumberInput(attrs={'class': 'form-control'}),
            'medida_de_plancha': forms.TextInput(attrs={'class': 'form-control'}),
        }

class RequisicionForm(forms.ModelForm):
    class Meta:
        model = RequisicionEncabezado
        fields = '__all__'
        widgets = {
            'numero_requisicion': forms.NumberInput(attrs={'class': 'form-control'}),
            'producto_a_elaborar': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'solicitado_por': forms.TextInput(attrs={'class': 'form-control'}),
            'autorizado_por': forms.TextInput(attrs={'class': 'form-control'}),
        }

# (Aquí pondremos el de ControlProceso más adelante)
# --- AGREGA ESTA NUEVA CLASE AL FINAL ---
class ControlProcesoForm(forms.ModelForm):
    class Meta:
        model = ControlProceso
        fields = '__all__'
        widgets = {
            'nombre_del_libro': forms.TextInput(attrs={'class': 'form-control'}),
            'temporada_anio': forms.NumberInput(attrs={'class': 'form-control'}),
            'tiraje': forms.NumberInput(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'elaborado_por': forms.TextInput(attrs={'class': 'form-control'}),
            'revisado_por': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ReporteDiarioForm(forms.ModelForm):
    class Meta:
        model = ReporteDiarioProductoTerminado
        fields = '__all__'
        widgets = {
            'nombre_encargado': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'turno': forms.TextInput(attrs={'class': 'form-control'}),
            'elaborado_por': forms.TextInput(attrs={'class': 'form-control'}),
            'revisado_por': forms.TextInput(attrs={'class': 'form-control'}),
        }

class NotaIngresoForm(forms.ModelForm):
    class Meta:
        model = NotaIngresoProductoTerminado
        fields = '__all__'
        widgets = {
            'numero_nota': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'elaborado_por': forms.TextInput(attrs={'class': 'form-control'}),
            'recibido_por': forms.TextInput(attrs={'class': 'form-control'}),
        }                       