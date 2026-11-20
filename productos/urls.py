
# URLs de la aplicación productos
from django.urls import path
from . import views

app_name = 'productos'

urlpatterns = [
    # Lista de productos
    path(
        '',
        views.ProductoListView.as_view(),
        name='lista'
    ),

    # Detalle de producto
    path(
        '<int:producto_id>/',
        views.ProductoDetailView.as_view(),
        name='detalle'
    ),

    # Crear producto
    path(
        'nuevo/',
        views.ProductoCreateView.as_view(),
        name='crear'
    ),

    # Editar producto
    path(
        '<int:producto_id>/editar/',
        views.ProductoUpdateView.as_view(),
        name='editar'
    ),

    # Eliminar producto
    path(
        '<int:producto_id>/eliminar/',
        views.ProductoDeleteView.as_view(),
        name='eliminar'
    ),

    # Exportar productos a Excel
    path(
        'exportar-excel/',
        views.exportar_productos_excel,
        name='exportar_excel'
    ),
]
