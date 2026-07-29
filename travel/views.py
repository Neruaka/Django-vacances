from django.shortcuts import render

from .models import Destination


def destination_list(request):
    """
    Page HTML publique (cahier des charges, point 7) : affiche toutes les
    destinations disponibles, sans passer par l'API JSON.
    """
    destinations = Destination.objects.all()
    return render(
        request,
        "travel/destination_list.html",
        {"destinations": destinations},
    )
