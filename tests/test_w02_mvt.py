"""
Suite de pruebas W02 — Patrón MVT:
templates, vistas y archivos estáticos.
"""

from django.test import TestCase
from django.urls import reverse


class TemplatesRenderTest(TestCase):
    """Verifica que las vistas usan los templates correctos."""

    def test_bienvenida_usa_template_correcto(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "bienvenida.html")

    def test_bienvenida_extiende_base(self):
        response = self.client.get("/")

        self.assertTemplateUsed(response, "base.html")

    def test_productos_usa_template_correcto(self):
        response = self.client.get(
            reverse("productos:inicio")
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "productos/index.html",
        )

    def test_clientes_usa_template_correcto(self):
        response = self.client.get(
            reverse("clientes:inicio")
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "clientes/index.html",
        )

    def test_proveedores_usa_template_correcto(self):
        response = self.client.get(
            reverse("proveedores:inicio")
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "proveedores/index.html",
        )

    def test_ventas_usa_template_correcto(self):
        response = self.client.get(
            reverse("ventas:inicio")
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "ventas/index.html",
        )

    def test_reportes_usa_template_correcto(self):
        response = self.client.get(
            reverse("reportes:inicio")
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "reportes/index.html",
        )


class ContextoBienvenidaTest(TestCase):
    """Verifica el contexto de la vista de bienvenida."""

    def test_contexto_contiene_modulos(self):
        response = self.client.get("/")

        self.assertIn(
            "modulos",
            response.context,
        )

    def test_contexto_tiene_seis_modulos(self):
        response = self.client.get("/")

        modulos = response.context.get(
            "modulos",
            [],
        )

        self.assertEqual(
            len(modulos),
            6,
        )


class StaticFilesConfigTest(TestCase):
    """Verifica estáticos y WhiteNoise."""

    def test_static_url_es_slash_static(self):
        from django.conf import settings

        self.assertEqual(
            settings.STATIC_URL,
            "/static/",
        )

    def test_static_root_configurado(self):
        from django.conf import settings

        self.assertTrue(
            bool(settings.STATIC_ROOT),
            "STATIC_ROOT no está configurado",
        )

    def test_whitenoise_en_middleware(self):
        from django.conf import settings

        self.assertIn(
            "whitenoise.middleware.WhiteNoiseMiddleware",
            settings.MIDDLEWARE,
            "WhiteNoise no está en MIDDLEWARE",
        )

    def test_whitenoise_despues_de_security(self):
        from django.conf import settings

        middleware = settings.MIDDLEWARE

        idx_security = middleware.index(
            "django.middleware.security.SecurityMiddleware"
        )

        idx_whitenoise = middleware.index(
            "whitenoise.middleware.WhiteNoiseMiddleware"
        )

        self.assertLess(
            idx_security,
            idx_whitenoise,
            "SecurityMiddleware debe ir ANTES que WhiteNoise",
        )