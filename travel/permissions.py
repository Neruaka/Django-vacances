from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthenticatedOrReadOnly(BasePermission):
    """
    Lecture (GET/HEAD/OPTIONS) : ouverte a tous, connectes ou non.
    Ecriture (POST/PUT/PATCH/DELETE) : reservee aux utilisateurs authentifies.

    C'est exactement la regle demandee par le cahier des charges (point 5) :
    "ecriture reservee aux utilisateurs authentifies (IsAuthenticatedOrReadOnly
    ou equivalent)". DRF fournit deja une classe du meme nom ; celle-ci est
    reecrite ici pour que le groupe puisse l'expliquer ligne par ligne en
    soutenance plutot que d'importer une boite noire.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)
