from django.shortcuts import render


def index(request):
    """
    Vista principal del módulo de productos.
    """

    context = {
        "titulo": "Productos",
        "descripcion": "Gestión de inventario y catálogo de productos.",
        "espiral": "Espiral 2 · W05",
    }

    return render(
        request,
        "productos/index.html",
        context,
    )