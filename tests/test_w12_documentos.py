
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from clientes.models import Cliente
from configuracion.models import ConfiguracionERP
from productos.models import Categoria, Producto
from ventas.models import DetalleVenta, Venta


class DocumentosW12Test(TestCase):

    def setUp(self):
        ConfiguracionERP.get_instance()

        self.user = User.objects.create_user(
            "docuser",
            password="pass",
        )

        categoria = Categoria.objects.create(
            nombre="Cat Doc",
        )

        producto = Producto.objects.create(
            nombre="Producto Doc",
            precio=Decimal("100.00"),
            stock=10,
            categoria=categoria,
        )

        cliente = Cliente.objects.create(
            nombre="Cliente Doc",
            correo="doc@test.com",
        )

        self.venta = Venta.objects.create(
            cliente=cliente,
        )

        DetalleVenta.objects.create(
            venta=self.venta,
            producto=producto,
            cantidad=2,
            precio_unitario=Decimal("100.00"),
        )

    def test_exportar_excel_autenticado(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("productos:exportar_excel")
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "spreadsheetml",
            response.get("Content-Type", ""),
        )

    def test_descargar_pdf_autenticado(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("ventas:pdf", args=[self.venta.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "application/pdf",
            response.get("Content-Type", ""),
        )
