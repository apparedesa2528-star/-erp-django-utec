from django.shortcuts import render


def index(request):
    """
    Vista principal del módulo de clientes.
    """

    context = {
        "titulo": "Clientes",
        "descripcion": "Gestión de cartera de clientes.",
        "espiral": "Espiral 2 · W04",
    }

    return render(
        request,
        "clientes/index.html",
        context,
    )