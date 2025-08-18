# produccion/forms.py
# Al principio de forms.py
from datetime import date
from django import forms
from .models import OrdenProduccion, RequisicionEncabezado, ControlProceso, ReporteDiarioProductoTerminado , NotaIngresoProductoTerminado,CorteDeBobina, CorteDeBobinaDetalle

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

# En tu archivo produccion/forms.py

class RequisicionForm(forms.ModelForm):
    class Meta:
        model = RequisicionEncabezado

        # --- ESTA ES LA LISTA CORREGIDA ---
        # Quitamos 'recibido' y agregamos 'producto_a_elaborar' para que coincida con tu modelo.
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

# (Aquí pondremos el de ControlProceso más adelante)
# --- AGREGA ESTA NUEVA CLASE AL FINAL ---
# En produccion/forms.py

class ControlProcesoForm(forms.ModelForm):
    class Meta:
        model = ControlProceso
        # Esta línea mágica le dice a Django que use todos los campos del modelo
        fields = '__all__'
        widgets = {
            # Aquí puedes mantener los widgets que ya tenías para darle estilo
            'orden_produccion': forms.Select(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'maquina': forms.TextInput(attrs={'class': 'form-control'}),
            'operario': forms.TextInput(attrs={'class': 'form-control'}),
            'hora_inicio': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'hora_final': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'pliegos_buenos': forms.NumberInput(attrs={'class': 'form-control'}),
            'pliegos_malos': forms.NumberInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
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

# En produccion/forms.py

class CorteDeBobinaForm(forms.ModelForm):
    class Meta:
        model = CorteDeBobina
        #fields = ['numero_reporte', 'fecha', 'nombre_operario', 'ancho_bobina', 'medida_de_corte']
        # AÑADE 'orden_produccion' A ESTA LISTA
        fields = ['orden_produccion', 'numero_reporte', 'fecha', 'nombre_operario', 'ancho_bobina', 'medida_de_corte']
        widgets = {
            # ... tus otros widgets ...
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    # --- AÑADE ESTE MÉTODO ---
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si el formulario es para un objeto nuevo (no para editar uno existente)
        if not self.instance.pk:
            # Ponemos la fecha de hoy como valor inicial
            self.fields['fecha'].initial = date.today()

class CorteDeBobinaDetalleForm(forms.ModelForm):
    class Meta:
        model = CorteDeBobinaDetalle
        fields = ['codigo_bobina', 'pliegos', 'resmas', 'observaciones']
        widgets = {
            # Usamos un <select> para que Select2 funcione correctamente
            'codigo_bobina': forms.Select(attrs={'class': 'form-control bobina-search', 'style': 'width: 100%;'}),
            'pliegos': forms.NumberInput(attrs={'class': 'form-control'}),
            'resmas': forms.NumberInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }                             