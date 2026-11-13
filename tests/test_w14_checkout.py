from decimal import Decimal
from unittest.mock import MagicMock, patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from clientes.models import Cliente
from configuracion.models import ConfiguracionERP
from productos.models import Categoria, Producto
from ventas.models import Pedido
class PagoExitosoTest(TestCase):
    """Tests de la vista pago_exitoso con Stripe simulado."""

    def setUp(self):
        ConfiguracionERP.get_instance()

        cat = Categoria.objects.create(nombre='C')

        self.prod = Producto.objects.create(
            nombre='P',
            precio=Decimal('100.00'),
            stock=5,
            categoria=cat
        )

        self.user = User.objects.create_user(
            'usuario_pago',
            password='pass',
            email='pago@test.com'
        )

        self.cli = Cliente.objects.create(
            nombre='C',
            correo='c@t.com'
        )

        self.pedido = Pedido.objects.create(
            numero_pedido='PED-2025-0001',
            cliente=self.cli,
            estado='pendiente',
            total_pagado=Decimal('116.00'),
            items_snapshot=[
                {
                    'producto_id': self.prod.pk,
                    'nombre': 'P',
                    'cantidad': 1,
                    'precio': '100.00',
                }
            ]
        )

        self.client.force_login(self.user)

    def crear_payment_intent_simulado(self):
        intent = MagicMock()

        intent.id = 'pi_test_123'
        intent.status = 'succeeded'
        intent.currency = 'mxn'
        intent.amount_received = 11600

        intent.metadata = {
            'pedido_id': str(self.pedido.pk),
            'pedido_num': self.pedido.numero_pedido,
        }

        return intent

    @patch('catalogo.views.stripe.PaymentIntent.retrieve')
    def test_pago_exitoso_devuelve_200(self, mock_retrieve):
        """Pago confirmado por Stripe devuelve HTTP 200."""

        mock_retrieve.return_value = (
            self.crear_payment_intent_simulado()
        )

        r = self.client.get(
            reverse(
                'catalogo:pago_exitoso',
                args=[self.pedido.pk]
            ),
            {'payment_intent': 'pi_test_123'}
        )

        self.assertEqual(r.status_code, 200)

    @patch('catalogo.views.stripe.PaymentIntent.retrieve')
    def test_pago_exitoso_vacia_carrito(self, mock_retrieve):
        """Un pago confirmado vacía el carrito."""

        mock_retrieve.return_value = (
            self.crear_payment_intent_simulado()
        )

        session = self.client.session

        session['carrito'] = {
            str(self.prod.pk): {
                'nombre': 'P',
                'precio': '100',
                'cantidad': 1,
            }
        }

        session.save()

        self.client.get(
            reverse(
                'catalogo:pago_exitoso',
                args=[self.pedido.pk]
            ),
            {'payment_intent': 'pi_test_123'}
        )

        self.assertEqual(
            self.client.session.get('carrito', {}),
            {}
        )

    @patch('catalogo.views.stripe.PaymentIntent.retrieve')
    def test_pago_exitoso_descuenta_stock(self, mock_retrieve):
        """El inventario disminuye después del pago confirmado."""

        mock_retrieve.return_value = (
            self.crear_payment_intent_simulado()
        )

        self.client.get(
            reverse(
                'catalogo:pago_exitoso',
                args=[self.pedido.pk]
            ),
            {'payment_intent': 'pi_test_123'}
        )

        self.prod.refresh_from_db()

        self.assertEqual(self.prod.stock, 4)

    @patch('catalogo.views.stripe.PaymentIntent.retrieve')
    def test_pago_exitoso_no_descuenta_dos_veces(self, mock_retrieve):
        """Volver a visitar el éxito no vuelve a descontar stock."""

        mock_retrieve.return_value = (
            self.crear_payment_intent_simulado()
        )

        url = reverse(
            'catalogo:pago_exitoso',
            args=[self.pedido.pk]
        )

        self.client.get(
            url,
            {'payment_intent': 'pi_test_123'}
        )

        self.client.get(
            url,
            {'payment_intent': 'pi_test_123'}
        )

        self.prod.refresh_from_db()

        self.assertEqual(self.prod.stock, 4)
