from django.shortcuts import render, get_object_or_404

from .models import Destination, TravelWish


def home(request):
    """
    Page d'accueil (modification 4) : vue d'ensemble du projet, avec le
    nombre de destinations et d'envies enregistrees, et des liens vers les
    listes detaillees.
    """
    context = {
        "destinations_count": Destination.objects.count(),
        "wishes_count": TravelWish.objects.count(),
    }
    return render(request, "home.html", context)


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


def destination_detail(request, pk):
    """
    Modification 1 : page HTML de detail pour UNE destination precise.
    Donnee publique (comme destination_list), pas de restriction d'acces.
    """
    destination = get_object_or_404(Destination, pk=pk)
    return render(
        request,
        "travel/destination_detail.html",
        {"destination": destination},
    )


def wish_list(request):
    """
    Page HTML listant TOUTES les envies, tous utilisateurs confondus.
    """
    wishes = TravelWish.objects.select_related("user", "destination").all()
    return render(
        request,
        "travel/wish_list.html",
        {"wishes": wishes},
    )


def wish_detail(request, pk):
    """
    Modification 1 : page HTML de detail pour UNE envie precise.
    """
    wish = get_object_or_404(TravelWish, pk=pk)
    return render(
        request,
        "travel/wish_detail.html",
        {"wish": wish},
    )
