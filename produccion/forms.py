# produccion/forms.py

from django import forms
from datetime import date
from django.db.models import Max
from .models import (
    OrdenProduccion, 
    RequisicionEncabezado, 
    ControlProceso, 
    ReporteDiarioProductoTerminado, 
    NotaIngresoProductoTerminado,
    CorteDeBobina, 
    CorteDeBobinaDetalle
)

# --- FORMULARIOS PRINCIPALES ---

class OrdenProduccionForm(forms.ModelForm):
    class Meta:
        model = OrdenProduccion
        fields = '__all__'
        # ... (puedes añadir widgets si los necesitas)

class RequisicionForm(forms.ModelForm):
    class Meta:
        model = RequisicionEncabezado
        fields = [
            'orden_produccion', 
            'numero_requisicion', 
            'producto_a_elaborar',
            'fecha', 
            'solicitado_por', 
            'autorizado_por'
        ]
        widgets = {
            'orden_produccion': forms.Select(attrs={'class': 'form-control'}),
            'numero_requisicion': forms.NumberInput(attrs={'class': 'form-control'}),
            'producto_a_elaborar': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'solicitado_por': forms.TextInput(attrs={'class': 'form-control'}),
            'autorizado_por': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ControlProcesoForm(forms.ModelForm):
    class Meta:
        model = ControlProceso
        fields = '__all__'
        # ... (puedes añadir widgets si los necesitas)

class ReporteDiarioForm(forms.ModelForm):
    class Meta:
        model = ReporteDiarioProductoTerminado
        fields = '__all__'
        # ... (puedes añadir widgets si los necesitas)

class NotaIngresoForm(forms.ModelForm):
    class Meta:
        model = NotaIngresoProductoTerminado
        fields = '__all__'
        # ... (puedes añadir widgets si los necesitas)

# --- FORMULARIOS PARA CORTE DE BOBINA ---

# En produccion/forms.py

# En produccion/forms.py
# En produccion/forms.py

class CorteDeBobinaForm(forms.ModelForm):
    class Meta:
        model = CorteDeBobina
        fields = [
            'orden_produccion', 'numero_reporte', 'fecha', 
            'nombre_operario', 'ancho_bobina', 'medida_de_corte'
        ]
        widgets = {
            'orden_produccion': forms.Select(attrs={'class': 'form-control'}),
            'numero_reporte': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'nombre_operario': forms.TextInput(attrs={'class': 'form-control'}),
            'ancho_bobina': forms.TextInput(attrs={'class': 'form-control'}),
            'medida_de_corte': forms.TextInput(attrs={'class': 'form-control'}),
        }
    # La función __init__ que teníamos aquí se ha eliminado.


# En produccion/forms.py
# --- ¡AQUÍ ESTÁ LA CORRECCIÓN! ---

class CorteDeBobinaDetalleForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        """
        Este es el truco mágico. Se ejecuta cuando se crea el formulario.
        """
        super().__init__(*args, **kwargs)
        
        # 1. Verificamos si estamos editando un objeto que ya existe
        if self.instance and self.instance.pk:
            
            # 2. Si hay un código de bobina guardado...
            if self.instance.codigo_bobina_usada:
                # ...lo ponemos como la única opción en el dropdown.
                self.fields['codigo_bobina_usada'].widget.choices = [
                    (self.instance.codigo_bobina_usada, self.instance.codigo_bobina_usada)
                ]
            
            # 3. Hacemos lo mismo para el primer pliego producido
            if self.instance.codigo_pliego_producido_1:
                self.fields['codigo_pliego_producido_1'].widget.choices = [
                    (self.instance.codigo_pliego_producido_1, self.instance.codigo_pliego_producido_1)
                ]

            # 4. Y también para el segundo pliego producido
            if self.instance.codigo_pliego_producido_2:
                self.fields['codigo_pliego_producido_2'].widget.choices = [
                    (self.instance.codigo_pliego_producido_2, self.instance.codigo_pliego_producido_2)
                ]

    class Meta:
        model = CorteDeBobinaDetalle
        fields = [
            'codigo_bobina_usada',
            'codigo_pliego_producido_1', 'cantidad_pliegos_1', 'resmas_producidas_1',
            'codigo_pliego_producido_2', 'cantidad_pliegos_2', 'resmas_producidas_2',
            'observaciones',
        ]
        # Esta parte se asegura que los campos tengan la clase CSS correcta
        # para que el JavaScript los encuentre.
        widgets = {
            'codigo_bobina_usada': forms.Select(attrs={'class': 'form-control bobina-search'}),
            'codigo_pliego_producido_1': forms.Select(attrs={'class': 'form-control papel-search'}),
            'codigo_pliego_producido_2': forms.Select(attrs={'class': 'form-control papel-search'}),
            'cantidad_pliegos_1': forms.NumberInput(attrs={'class': 'form-control'}),
            'resmas_producidas_1': forms.NumberInput(attrs={'class': 'form-control'}),
            'cantidad_pliegos_2': forms.NumberInput(attrs={'class': 'form-control'}),
            'resmas_producidas_2': forms.NumberInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }



# Formulario para "EDITAR" con campos de texto simples
class CorteDeBobinaDetalleFormEditar(forms.ModelForm):
    class Meta:
        model = CorteDeBobinaDetalle
        fields = '__all__'
        exclude = ('corte_de_bobina',)
        widgets = {
            'codigo_bobina_usada': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_pliego_producido_1': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_pliego_producido_2': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad_pliegos_1': forms.NumberInput(attrs={'class': 'form-control'}),
            'resmas_producidas_1': forms.NumberInput(attrs={'class': 'form-control'}),
            'cantidad_pliegos_2': forms.NumberInput(attrs={'class': 'form-control'}),
            'resmas_producidas_2': forms.NumberInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }