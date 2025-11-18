from django import forms
from django.forms import inlineformset_factory
from .models import Liquidacion, LiquidacionDetalle

class LiquidacionForm(forms.ModelForm):
    class Meta:
        model = Liquidacion
        fields = ['cliente', 'fecha', 'referencia']


class LiquidacionDetalleForm(forms.ModelForm):
    class Meta:
        model = LiquidacionDetalle
        fields = ['producto', 'devolucion', 'venta', 'saldo', 'precio']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control producto-search'}),
            'devolucion': forms.NumberInput(attrs={'class': 'form-control devolucion'}),
            'venta': forms.NumberInput(attrs={'class': 'form-control venta'}),
            'saldo': forms.NumberInput(attrs={'class': 'form-control saldo'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control precio'}),
        }


LiquidacionDetalleFormSet = inlineformset_factory(
    Liquidacion,
    LiquidacionDetalle,
    form=LiquidacionDetalleForm,
    extra=1,
    can_delete=True
)
