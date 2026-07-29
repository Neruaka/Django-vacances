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

    ATTENTION - choix de conception a connaitre : contrairement a l'API
    (/api/wishes/), qui filtre strictement par request.user (chacun ne
    voit que ses propres envies via un jeton JWT), cette page HTML n'a pas
    de mecanisme de connexion par session pour l'instant. Elle affiche donc
    toutes les envies de tous les utilisateurs, sans filtrage. C'est un
    ecart volontaire et documente par rapport a la logique de vie privee de
    l'API - a mentionner si demande en soutenance.
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
    Meme remarque que wish_list : pas de filtrage par utilisateur ici,
    contrairement a l'API JSON qui reste strictement privee.
    """
    wish = get_object_or_404(TravelWish, pk=pk)
    return render(
        request,
        "travel/wish_detail.html",
        {"wish": wish},
    )
