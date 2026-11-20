
from decimal import Decimal, InvalidOperation

from django import forms
from .models import Producto


class ProductoForm(forms.ModelForm):

    class Meta:
        model = Producto

        fields = [
            'nombre',
            'precio',
            'stock',
            'categoria',
            'proveedor',
            'activo',
            'imagen',
        ]

        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'erp-input',
                'placeholder': 'Nombre del producto',
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'erp-input',
                'step': '0.01',
                'min': '0',
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'erp-input',
                'min': '0',
            }),
            'categoria': forms.Select(attrs={
                'class': 'erp-input',
            }),
            'proveedor': forms.Select(attrs={
                'class': 'erp-input',
            }),
            'imagen': forms.ClearableFileInput(attrs={
                'class': 'erp-input',
                'accept': 'image/jpeg,image/png,image/webp',
            }),
        }

        labels = {
            'nombre': 'Nombre',
            'precio': 'Precio ($)',
            'stock': 'Stock disponible',
            'categoria': 'Categoría',
            'proveedor': 'Proveedor',
            'activo': 'Activo',
            'imagen': 'Imagen del producto',
        }

    def clean(self):
        cleaned_data = super().clean()

        precio_original = self.data.get('precio')

        try:
            precio = Decimal(str(precio_original))
        except (InvalidOperation, TypeError, ValueError):
            return cleaned_data

        if precio < Decimal('0.00'):
            self.errors.pop('precio', None)

            self.add_error(
                'precio',
                forms.ValidationError(
                    'Asegúrese de que este valor sea mayor o igual a 0.00.'
                )
            )

            self.add_error(
                'precio',
                forms.ValidationError(
                    f'El precio no puede ser negativo. Valor recibido: {precio:.2f}'
                )
            )

        return cleaned_data
