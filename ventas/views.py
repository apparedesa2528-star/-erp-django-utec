from django.shortcuts import render


def index(request):
    """
    Vista principal del módulo de ventas.
    """

    context = {
        "titulo": "Ventas",
        "descripcion": "Ciclo de ventas, pedidos y facturación.",
        "espiral": "Espiral 3 · W07",
    }

    return render(
        request,
        "ventas/index.html",
        context,
    )