"""Modelos de la app ventas — ERP Django."""


from decimal import Decimal


from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


from clientes.models import Cliente
from productos.models import Producto




# ============================================================
# VENTA
# ============================================================


class Venta(models.Model):
    """Encabezado de una venta interna."""


    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name='ventas',
        verbose_name='Cliente'
    )


    fecha = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha'
    )


    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['-fecha']


    def __str__(self):
        return (
            f"Venta #{self.pk} — "
            f"{self.cliente} ({self.fecha:%d/%m/%Y})"
        )


    @property
    def total(self):
        """Calcula el total de la venta."""


        return sum(
            (detalle.subtotal for detalle in self.detalles.all()),
            Decimal('0.00')
        )




# ============================================================
# DETALLE DE VENTA
# ============================================================


class DetalleVenta(models.Model):
    """Producto y cantidad incluidos en una venta."""


    venta = models.ForeignKey(
        Venta,
        on_delete=models.CASCADE,
        related_name='detalles',
        verbose_name='Venta'
    )


    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        related_name='detalles_venta',
        verbose_name='Producto'
    )


    cantidad = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Cantidad'
    )


    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Precio unitario',
        help_text='Precio del producto al momento de la venta.'
    )


    class Meta:
        verbose_name = 'Detalle de venta'
        verbose_name_plural = 'Detalles de venta'


    def __str__(self):
        return f"{self.producto.nombre} × {self.cantidad}"


    @property
    def subtotal(self):
        """Calcula el subtotal de esta línea."""


        return self.precio_unitario * self.cantidad


    def save(self, *args, **kwargs):
        """Guarda el precio actual si no se especificó."""


        if self.precio_unitario is None:
            self.precio_unitario = self.producto.precio


        super().save(*args, **kwargs)


    def clean(self):
        """Valida la cantidad."""


        if self.cantidad is not None and self.cantidad < 1:
            raise ValidationError({
                'cantidad': 'La cantidad debe ser al menos 1.'
            })




# ============================================================
# PEDIDO DE COMERCIO ELECTRÓNICO
# ============================================================


class Pedido(models.Model):
    """Pedido realizado desde el catálogo público."""


    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente de pago'),
        ('pagado', 'Pago confirmado'),
        ('enviado', 'En camino'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]


    numero_pedido = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Número de pedido',
        help_text='Formato sugerido: PED-YYYY-NNNN'
    )


    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name='pedidos',
        verbose_name='Cliente'
    )


    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='pendiente',
        verbose_name='Estado'
    )


    fecha_pedido = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha del pedido'
    )


    fecha_entrega = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fecha de entrega'
    )


    total_pagado = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Total pagado'
    )


    # Copia de los productos comprados.
    # Se utiliza para descontar el inventario después
    # de confirmar el pago con Stripe.


    items_snapshot = models.JSONField(
        default=list,
        blank=True,
        verbose_name='Productos del pedido',
        help_text=(
            'Copia de los productos, cantidades y precios '
            'al momento de crear el pedido.'
        )
    )


    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-fecha_pedido']


    def __str__(self):
        return (
            f"{self.numero_pedido} — {self.cliente} "
            f"[{self.get_estado_display()}]"
        )


    def clean(self):
        """Valida que la entrega no sea anterior al pedido."""


        if (
            self.fecha_entrega
            and self.fecha_pedido
            and self.fecha_entrega < self.fecha_pedido.date()
        ):
            raise ValidationError({
                'fecha_entrega': (
                    'La fecha de entrega no puede ser anterior '
                    'a la fecha del pedido.'
                )
            })