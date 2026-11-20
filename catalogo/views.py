from ventas.tasks import enviar_confirmacion_pedido
import stripe
import stripe.apps
import stripe.billing_portal
import stripe.checkout
import stripe.climate
import stripe.financial_connections
import stripe.identity
import stripe.issuing
import stripe.radar
import stripe.reporting
import stripe.sigma
import stripe.tax
import stripe.terminal
import stripe.test_helpers
import stripe.treasury


from decimal import Decimal, ROUND_HALF_UP


from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView


from productos.models import Producto
from ventas.models import Pedido


from .checkout_utils import (
    calcular_totales,
    generar_numero_pedido,
    obtener_o_crear_cliente,
)


from .filters import ProductoFilter




# ============================================================
# CONFIGURACIÓN DE STRIPE
# ============================================================


stripe.api_key = settings.STRIPE_SECRET_KEY




# ============================================================
# CATÁLOGO PÚBLICO
# ============================================================


class CatalogoView(ListView):
    """Catálogo público de productos con filtros."""


    model = Producto
    template_name = 'catalogo/catalogo.html'
    context_object_name = 'productos'
    paginate_by = 12


    def get_queryset(self):
        qs = (
            Producto.objects
            .select_related('categoria', 'proveedor')
            .filter(activo=True)
            .order_by('nombre')
        )


        self.filtro = ProductoFilter(
            self.request.GET,
            queryset=qs
        )


        return self.filtro.qs


    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)


        ctx['filtro'] = self.filtro
        ctx['categorias'] = (
            self.filtro.form.fields['categoria'].queryset
        )


        return ctx




# ============================================================
# CARRITO DE COMPRAS
# ============================================================


def _obtener_carrito(request) -> dict:
    """Obtiene el carrito almacenado en la sesión."""


    return request.session.get('carrito', {})




def _guardar_carrito(request, carrito: dict) -> None:
    """Guarda los cambios del carrito en la sesión."""


    request.session['carrito'] = carrito
    request.session.modified = True




def ver_carrito(request):
    """Muestra los productos agregados al carrito."""


    carrito = _obtener_carrito(request)


    items = []
    total = Decimal('0.00')


    for prod_id, datos in carrito.items():
        precio = Decimal(str(datos['precio']))
        cantidad = int(datos['cantidad'])
        subtotal = precio * cantidad


        total += subtotal


        items.append({
            'prod_id': prod_id,
            'nombre': datos['nombre'],
            'precio': precio,
            'cantidad': cantidad,
            'subtotal': subtotal,
            'imagen': datos.get('imagen'),
        })


    return render(
        request,
        'catalogo/carrito.html',
        {
            'items': items,
            'total': total,
        }
    )




def agregar_al_carrito(request, producto_id: int):
    """Agrega un producto al carrito."""


    if request.method != 'POST':
        return redirect('catalogo:catalogo')


    producto = get_object_or_404(
        Producto,
        pk=producto_id,
        activo=True
    )


    try:
        cantidad = int(request.POST.get('cantidad', 1))
    except (TypeError, ValueError):
        cantidad = 1


    if cantidad < 1:
        messages.error(
            request,
            'La cantidad debe ser mayor que cero.'
        )
        return redirect('catalogo:catalogo')


    if cantidad > producto.stock:
        messages.error(
            request,
            f'Solo hay {producto.stock} unidades disponibles '
            f'de {producto.nombre}.'
        )
        return redirect('catalogo:catalogo')


    carrito = _obtener_carrito(request)
    clave = str(producto_id)


    cantidad_actual = int(
        carrito.get(clave, {}).get('cantidad', 0)
    )


    if cantidad_actual + cantidad > producto.stock:
        messages.error(
            request,
            f'No hay suficiente stock de {producto.nombre}. '
            f'Disponibles: {producto.stock}.'
        )
        return redirect('catalogo:catalogo')


    if clave in carrito:
        carrito[clave]['cantidad'] += cantidad
    else:
        carrito[clave] = {
            'nombre': producto.nombre,
            'precio': str(producto.precio),
            'cantidad': cantidad,
            'imagen': (
                producto.imagen.name
                if producto.imagen else None
            ),
        }


    _guardar_carrito(request, carrito)


    messages.success(
        request,
        f'"{producto.nombre}" agregado al carrito.'
    )


    next_url = (
        request.POST.get('next')
        or request.META.get('HTTP_REFERER')
    )


    return redirect(next_url or 'catalogo:catalogo')




def remover_del_carrito(request, producto_id: int):
    """Elimina un producto del carrito."""


    if request.method != 'POST':
        return redirect('catalogo:carrito')


    carrito = _obtener_carrito(request)
    clave = str(producto_id)


    nombre = carrito.get(
        clave, {}
    ).get('nombre', 'Producto')


    carrito.pop(clave, None)


    _guardar_carrito(request, carrito)


    messages.warning(
        request,
        f'"{nombre}" eliminado del carrito.'
    )


    return redirect('catalogo:carrito')




def actualizar_cantidad(request, producto_id: int):
    """Actualiza la cantidad de un producto."""


    if request.method != 'POST':
        return redirect('catalogo:carrito')


    carrito = _obtener_carrito(request)
    clave = str(producto_id)


    try:
        cantidad = int(request.POST.get('cantidad', 1))
    except (TypeError, ValueError):
        cantidad = 1


    if clave in carrito:
        producto = get_object_or_404(
            Producto,
            pk=producto_id,
            activo=True
        )


        if cantidad > producto.stock:
            messages.error(
                request,
                f'Solo hay {producto.stock} unidades disponibles.'
            )
            return redirect('catalogo:carrito')


        if cantidad > 0:
            carrito[clave]['cantidad'] = cantidad
        else:
            carrito.pop(clave)


        _guardar_carrito(request, carrito)


    return redirect('catalogo:carrito')




def vaciar_carrito(request):
    """Vacía completamente el carrito."""


    if request.method == 'POST':
        _guardar_carrito(request, {})


        messages.info(request, 'Carrito vaciado.')


    return redirect('catalogo:carrito')




# ============================================================
# CHECKOUT Y PAGOS CON STRIPE
# ============================================================


@login_required
def checkout(request):
    """Genera el pedido y el PaymentIntent de Stripe."""


    carrito = _obtener_carrito(request)


    if not carrito:
        messages.warning(request, 'Tu carrito está vacío.')
        return redirect('catalogo:catalogo')


    totales = calcular_totales(carrito)
    publishable_key = settings.STRIPE_PUBLISHABLE_KEY


    if not settings.STRIPE_SECRET_KEY or not publishable_key:
        messages.error(
            request,
            'Stripe no está configurado correctamente.'
        )
        return redirect('catalogo:carrito')


    if request.method == 'GET':
        return render(
            request,
            'catalogo/checkout.html',
            {
                'carrito': carrito,
                'totales': totales,
                'pedido': None,
                'client_secret': None,
                'publishable_key': publishable_key,
            }
        )


    if request.method == 'POST':


        total = Decimal(str(totales['total']))


        if total < Decimal('10.00'):
            messages.error(
                request,
                'El importe mínimo para pagar con Stripe '
                'es de $10.00 MXN.'
            )
            return redirect('catalogo:carrito')


        try:
            # Crear una copia de los productos comprados.
            # Esta copia permitirá descontar el stock después
            # de confirmar el pago, aunque se vacíe el carrito.


            snapshot = []


            for producto_id, datos in carrito.items():


                producto = get_object_or_404(
                    Producto,
                    pk=int(producto_id),
                    activo=True
                )


                cantidad = int(datos['cantidad'])


                if cantidad < 1:
                    raise ValueError(
                        f'Cantidad inválida para {producto.nombre}.'
                    )


                if producto.stock < cantidad:
                    raise ValueError(
                        f'Stock insuficiente de {producto.nombre}. '
                        f'Disponibles: {producto.stock}.'
                    )


                snapshot.append({
                    'producto_id': producto.pk,
                    'nombre': producto.nombre,
                    'cantidad': cantidad,
                    'precio': str(producto.precio),
                })


            if not snapshot:
                raise ValueError('No hay productos válidos en el pedido.')


            cliente = obtener_o_crear_cliente(request.user)


            numero = generar_numero_pedido()


            monto_centavos = int(
                (total * 100).quantize(
                    Decimal('1'),
                    rounding=ROUND_HALF_UP
                )
            )


            # Crear pedido pendiente con copia de los productos.
            pedido = Pedido.objects.create(
                numero_pedido=numero,
                cliente=cliente,
                estado='pendiente',
                total_pagado=total,
                items_snapshot=snapshot,
            )


            # Crear PaymentIntent.
            # La clave incluye pedido e importe para evitar
            # conflictos de idempotencia con parámetros diferentes.


            intent = stripe.PaymentIntent.create(
                amount=monto_centavos,
                currency='mxn',
                metadata={
                    'pedido_id': str(pedido.pk),
                    'pedido_num': str(pedido.numero_pedido),
                    'cliente': str(cliente.nombre),
                },
                idempotency_key=(
                    f'pedido-{pedido.pk}-mxn-{monto_centavos}'
                ),
            )


            return render(
                request,
                'catalogo/checkout.html',
                {
                    'carrito': carrito,
                    'totales': totales,
                    'pedido': pedido,
                    'client_secret': intent.client_secret,
                    'publishable_key': publishable_key,
                }
            )


        except stripe.error.StripeError as exc:
            import traceback
            traceback.print_exc()


            messages.error(
                request,
                f'Error de Stripe: {str(exc)}'
            )


            return redirect('catalogo:pago_error')


        except Exception as exc:
            import traceback
            traceback.print_exc()


            messages.error(
                request,
                f'Error al iniciar el pago: {str(exc)}'
            )


            return redirect('catalogo:pago_error')


    return redirect('catalogo:checkout')




# ============================================================
# CONFIRMACIÓN DE PAGO Y DESCUENTO DE INVENTARIO
# ============================================================


@login_required
def pago_exitoso(request, pedido_id: int):
    """Vista de confirmación post-pago exitoso — W16.

    Cambios respecto a W14:
        Dispara la tarea asíncrona de correo con .delay().
        La tarea se encola en Redis y el worker la procesa
        en segundo plano, sin bloquear esta respuesta HTTP.
    """
    from django.shortcuts import get_object_or_404
    pedido = get_object_or_404(Pedido, pk=pedido_id)

    # Vaciar el carrito de la sesión
    _guardar_carrito(request, {})

    # ── NUEVO W16: disparar tarea asíncrona de confirmación ───────────
    # .delay() envía la tarea al broker Redis de forma no bloqueante.
    # El worker la ejecutará en segundo plano.
    enviar_confirmacion_pedido.delay(pedido.pk)
    # ──────────────────────────────────────────────────────────────────

    messages.success(
        request,
        f'¡Pago exitoso! Tu pedido {pedido.numero_pedido} '
        f'está confirmado. Recibirás un correo de confirmación pronto.'
    )

    return render(request, 'catalogo/pago_exitoso.html', {
        'pedido': pedido,
    })
# ============================================================
# ERROR DE PAGO
# ============================================================


def pago_error(request):
    """Muestra la página de error de pago."""


    return render(
        request,
        'catalogo/pago_error.html'
    )