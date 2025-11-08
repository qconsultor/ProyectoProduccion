from django.forms import BaseInlineFormSet, inlineformset_factory
from .models import Consignacion, ConsignacionDetalle
from .forms import ConsignacionDetalleForm  # usa tu formulario actual


class ConsignacionDetalleBaseFormSet(BaseInlineFormSet):
    def clean(self):
        """Ignorar filas totalmente vacías en el formset."""
        super().clean()
        for form in self.forms:
            producto = form.cleaned_data.get('producto')
            cantidad = form.cleaned_data.get('cantidad')
            precio = form.cleaned_data.get('precio')
            print(f"🧾 Limpieza de formulario — producto={producto}, cantidad={cantidad}, precio={precio}")
            # Si los tres están vacíos, marcar para eliminar
            if not producto and not cantidad and not precio:
                form.cleaned_data['DELETE'] = True


ConsignacionDetalleFormSet = inlineformset_factory(
    Consignacion,
    ConsignacionDetalle,
    form=ConsignacionDetalleForm,
    formset=ConsignacionDetalleBaseFormSet,  # 👈 NUEVA CLASE BASE
    extra=1,
    can_delete=True
)
