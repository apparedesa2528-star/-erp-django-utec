from django.contrib import admin
from django.urls import include, path

from . import views


urlpatterns = [
    path("", views.bienvenida, name="bienvenida"),

    path(
        "productos/",
        include("productos.urls"),
    ),

    path(
        "clientes/",
        include("clientes.urls"),
    ),

    path(
        "proveedores/",
        include("proveedores.urls"),
    ),

    path(
        "ventas/",
        include("ventas.urls"),
    ),

    path(
        "reportes/",
        include("reportes.urls"),
    ),

    path("admin/", admin.site.urls),
]