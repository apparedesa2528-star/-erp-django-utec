"""Modelos de la aplicación productos."""


from decimal import Decimal


from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


from proveedores.models import Proveedor
from .validators import validar_imagen_producto




class Categoria(models.Model):
    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nombre"
    )


    descripcion = models.TextField(
        blank=True,
        verbose_name="Descripción"
    )


    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ["nombre"]


    def __str__(self):
        return self.nombre




class Producto(models.Model):
    nombre = models.CharField(
        max_length=150,
        verbose_name="Nombre"
    )


    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        verbose_name="Precio"
    )


    stock = models.PositiveIntegerField(
        default=0,
        verbose_name="Existencias"
    )


    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="productos",
        verbose_name="Categoría"
    )


    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="productos",
        verbose_name="Proveedor"
    )


    activo = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )


    imagen = models.ImageField(
        upload_to="productos/",
        null=True,
        blank=True,
        validators=[validar_imagen_producto],
        verbose_name="Imagen"
    )


    creado = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )


    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ["nombre"]


    def clean(self):
        super().clean()


        if self.precio is not None and self.precio < Decimal("0.00"):
            raise ValidationError({
                "precio": "El precio no puede ser negativo."
            })


        if self.stock is not None and self.stock < 0:
            raise ValidationError({
                "stock": "El inventario no puede ser negativo."
            })


    def __str__(self):
        return f"{self.nombre} (${self.precio})"