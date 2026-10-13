from django.shortcuts import render
from django.urls import reverse


def bienvenida(request):
    """
    Página de inicio del ERP.

    Muestra las tarjetas de los diferentes módulos
    del sistema.
    """

    modulos = [
        {
            "nombre": "Productos",
            "icono": "📦",
            "url": reverse("productos:inicio"),
            "descripcion": "Inventario, precios y stock",
        },
        {
            "nombre": "Clientes",
            "icono": "👥",
            "url": reverse("clientes:inicio"),
            "descripcion": "Cartera y gestión de clientes",
        },
        {
            "nombre": "Proveedores",
            "icono": "🏭",
            "url": reverse("proveedores:inicio"),
            "descripcion": "Red de proveedores",
        },
        {
            "nombre": "Ventas",
            "icono": "💰",
            "url": reverse("ventas:inicio"),
            "descripcion": "Pedidos, facturas y cobros",
        },
        {
            "nombre": "Reportes",
            "icono": "📊",
            "url": reverse("reportes:inicio"),
            "descripcion": "Dashboard y analítica",
        },
        {
            "nombre": "Admin",
            "icono": "⚙️",
            "url": "/admin/",
            "descripcion": "Panel de administración Django",
        },
    ]

    return render(
        request,
        "bienvenida.html",
        {"modulos": modulos},
    )