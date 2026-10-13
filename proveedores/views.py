from django.shortcuts import render


def index(request):
    """
    Vista principal del módulo de proveedores.
    """

    context = {
        "titulo": "Proveedores",
        "descripcion": "Red de proveedores de mercancía.",
        "espiral": "Espiral 2 · W04",
    }

    return render(
        request,
        "proveedores/index.html",
        context,
    )