# produccion/forms_liquidacion.py
from django import forms
from django.forms import BaseInlineFormSet, inlineformset_factory
from .models_liquidacion import Liquidacion, LiquidacionDetalle


# -----------------------------------------------------
# FORMULARIO PRINCIPAL
# -----------------------------------------------------
class LiquidacionForm(forms.ModelForm):
    class Meta:
        model = Liquidacion
        fields = ['cliente_id', 'fecha', 'referencia']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'referencia': forms.TextInput(attrs={'class': 'form-control'}),
            'cliente_id': forms.HiddenInput(),  # se llena con Select2 visible
        }


# -----------------------------------------------------
# FORMULARIO DETALLE (líneas de productos)
# -----------------------------------------------------
class LiquidacionDetalleForm(forms.ModelForm):
    class Meta:
        model = LiquidacionDetalle
        exclude = ()
        widgets = {
            'producto_id': forms.TextInput(attrs={'class': 'form-control producto-id-input', 'readonly': True}),
            'devolucion': forms.NumberInput(attrs={'class': 'form-control devolucion'}),
            'venta': forms.NumberInput(attrs={'class': 'form-control venta'}),
            'saldo': forms.NumberInput(attrs={'class': 'form-control saldo', 'readonly': True}),
            'precio': forms.NumberInput(attrs={'class': 'form-control precio'}),
        }

    def clean(self):
        cleaned = super().clean()
        return cleaned


# -----------------------------------------------------
# BASE FORMSET PERSONALIZADO
# -----------------------------------------------------
class LiquidacionDetalleBaseFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        for form in self.forms:
            if not hasattr(form, 'cleaned_data'):
                continue
            producto = form.cleaned_data.get('producto_id')
            devolucion = form.cleaned_data.get('devolucion')
            venta = form.cleaned_data.get('venta')
            precio = form.cleaned_data.get('precio')

            # marcar como vacía si no tiene datos
            if not producto and not devolucion and not venta and not precio:
                form.cleaned_data['DELETE'] = True


# -----------------------------------------------------
# FORMSET FINAL (para usar en la vista)
# -----------------------------------------------------
LiquidacionDetalleFormSet = inlineformset_factory(
    Liquidacion,
    LiquidacionDetalle,
    form=LiquidacionDetalleForm,
    formset=LiquidacionDetalleBaseFormSet,
    extra=1,
    can_delete=True,
    min_num=0,
    validate_min=False
)
