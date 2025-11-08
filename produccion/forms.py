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
    CorteDeBobinaDetalle,
    Producto,
    ControlProcesoDetalle,
    
    # --- MODELOS AÑADIDOS A LA IMPORTACIÓN ---
    Cliente, # <--- ¡EL QUE FALTABA!
    Consignacion,
    ConsignacionDetalle,
)

# --- FORMULARIOS PRINCIPALES ---

class OrdenProduccionForm(forms.ModelForm):
    class Meta:
        model = OrdenProduccion
        fields = '__all__'


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
        labels = {
            'temporada_anio': 'Temporada/Año',
        }


class ReporteDiarioForm(forms.ModelForm):
    class Meta:
        model = ReporteDiarioProductoTerminado
        fields = '__all__'


class NotaIngresoForm(forms.ModelForm):
    class Meta:
        model = NotaIngresoProductoTerminado
        fields = '__all__'


# --- FORMULARIOS PARA CORTE DE BOBINA ---

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


class CorteDeBobinaDetalleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.codigo_bobina_usada:
                self.fields['codigo_bobina_usada'].widget.choices = [
                    (self.instance.codigo_bobina_usada, self.instance.codigo_bobina_usada)
                ]
            if self.instance.codigo_pliego_producido_1:
                self.fields['codigo_pliego_producido_1'].widget.choices = [
                    (self.instance.codigo_pliego_producido_1, self.instance.codigo_pliego_producido_1)
                ]
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


# --- FORMULARIO PRODUCTO ---
class ProductoForm(forms.ModelForm):
    nombre3 = forms.ChoiceField(
        label="Tipo de Producto",
        choices=[
            ('BOBINA', 'Bobina'),
            ('PAPEL', 'Papel'),
            ('QUIMICO', 'Químico'),
        ],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Producto
        fields = ['codigo', 'nombre', 'nombre3']
        widgets = {
            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código único del producto'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre descriptivo del producto'
            }),
        }


class ControlProcesoDetalleForm(forms.ModelForm):
    class Meta:
        model = ControlProcesoDetalle
        fields = ['fecha', 'turno', 'compaginado', 'doblado_libro', 'doblado_portada',
                  'engrapado', 'pegado', 'refilado', 'empacado', 'unidades']
        widgets = {
            'fecha': forms.DateInput(attrs={'class': 'form-control form-control-sm', 'type': 'date'}),
            'turno': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'compaginado': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'doblado_libro': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'doblado_portada': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'engrapado': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'pegado': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'refilado': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'empacado': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'unidades': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
        }

# ==============================================================================
# FORMULARIOS PARA EL MÓDULO DE CONSIGNACIONES
# ==============================================================================

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['codigo', 'nombre', 'nombrecomercial']

class ConsignacionForm(forms.ModelForm):
    cliente_search = forms.CharField(
        label="Cliente",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Busca por código o nombre...'}),
        required=False
    )

    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.using('rq').filter(empresa=10),   # 👈 FILTRAMOS AQUÍ
        to_field_name='codigo',
        empty_label="Seleccione un cliente",
    )

    class Meta:
        model = Consignacion
        fields = ['cliente', 'fecha', 'referencia']
        widgets = {
            'referencia': forms.TextInput(attrs={'readonly': 'readonly'}),
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # --- Al editar ---
        if self.instance and self.instance.pk:
            cliente_codigo = getattr(self.instance, 'cliente_id', None)
            if cliente_codigo:
                try:
                    cliente_obj = Cliente.objects.using('rq').filter(empresa=10).get(codigo=cliente_codigo)
                    self.fields['cliente_search'].initial = f"{cliente_obj.nombre} ({cliente_obj.codigo})"
                    self.initial['cliente'] = cliente_obj
                except Cliente.DoesNotExist:
                    self.fields['cliente_search'].initial = f"Cliente {cliente_codigo} no encontrado"
                except Cliente.MultipleObjectsReturned:
                    self.fields['cliente_search'].initial = f"⚠️ Código duplicado en otra empresa"

# class ConsignacionForm(forms.ModelForm):
#     # Campo para el buscador visual (no se guarda directamente)
#     cliente_search = forms.CharField(
#         label="Cliente",
#         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Busca por código o nombre...'}),
#         required=False 
#     )

#     cliente = forms.ModelChoiceField(
#         queryset=Cliente.objects.using('rq').filter(empresa=10),  # 👈 aquí filtras solo los de sucursal 10 #queryset=Cliente.objects.using('rq').all(),  # 👈 usar la misma base
#         to_field_name='codigo',
#         empty_label="Seleccione un cliente",
#     )

#     class Meta:
#         model = Consignacion
#         fields = ['cliente', 'fecha', 'referencia']
#         widgets = {
#             'referencia': forms.TextInput(attrs={'readonly': 'readonly'}),
#             'fecha': forms.DateInput(attrs={'type': 'date'}),
#         }

#     # 3. Ya NO necesitamos configurar 'cliente' en __init__

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
        
#         # --- Lógica para mostrar el nombre si estamos editando ---
#         if self.instance and self.instance.pk:
#             # Obtenemos el código de cliente guardado ('cliente_id' es el nombre por defecto)
#             cliente_codigo = getattr(self.instance, 'cliente_id', None) 
#             if cliente_codigo:
#                 try:
#                     # Buscamos el objeto Cliente en 'rq' usando el código
#                     cliente_obj = Cliente.objects.using('rq').get(codigo=cliente_codigo)
#                     # Ponemos el texto en el buscador visible
#                     self.fields['cliente_search'].initial = f"{cliente_obj.nombre} ({cliente_obj.codigo})"
#                     # Ponemos el OBJETO Cliente como valor inicial del campo 'cliente'
#                     self.initial['cliente'] = cliente_obj 
#                 except Cliente.DoesNotExist:
#                     self.fields['cliente_search'].initial = f"Cliente {cliente_codigo} no encontrado en DB 'rq'"
#                 except Cliente.MultipleObjectsReturned:
#                      self.fields['cliente_search'].initial = f"ERROR: Múltiples clientes con código {cliente_codigo} en DB 'rq'"
#             else:
#                  self.fields['cliente_search'].initial = "Cliente no especificado"
#         # --- Fin lógica de edición ---


from decimal import Decimal, ROUND_HALF_UP

class ConsignacionDetalleForm(forms.ModelForm):
    producto = forms.ModelChoiceField(
        queryset=Producto.objects.using('rq').all(),
        widget=forms.HiddenInput()
    )

    class Meta:
        model = ConsignacionDetalle
        fields = ['producto', 'cantidad', 'precio', 'total_linea']
        widgets = {
            'cantidad': forms.NumberInput(attrs={'class': 'form-control cantidad'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control precio'}),
            'total_linea': forms.NumberInput(
                attrs={'class': 'form-control total-linea', 'readonly': 'readonly'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['total_linea'].required = False  # 👈 evitar error required

    def clean_id(self):
        """Permite guardar líneas nuevas sin tener campo 'id' en el POST."""
        return self.cleaned_data.get('id', None)

    def clean_total_linea(self):
        """Calcula y redondea el total con 2 decimales."""
        cantidad = self.cleaned_data.get('cantidad') or 0
        precio = self.cleaned_data.get('precio') or 0
        total = Decimal(cantidad) * Decimal(precio)
        return total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

# Usamos el nombre correcto: ConsignacionDetalle
DetalleConsignacionFormSet = forms.inlineformset_factory(
    Consignacion,
    ConsignacionDetalle,
    form=ConsignacionDetalleForm,
    fields='__all__',
    extra=1,
    can_delete=True,
    fk_name='consignacion',
)

    
#07112025
# ===============================
# 🧩 FormSet personalizado
# ===============================
from django.forms import BaseInlineFormSet

class ConsignacionDetalleBaseFormSet(BaseInlineFormSet):
    def clean(self):
        """Ignorar filas totalmente vacías en el formset"""
        super().clean()
        for form in self.forms:
            producto = form.cleaned_data.get('producto')
            cantidad = form.cleaned_data.get('cantidad')
            precio = form.cleaned_data.get('precio')

            # Si los tres están vacíos, no validar este form
            if not producto and not cantidad and not precio:
                form.cleaned_data['DELETE'] = True

