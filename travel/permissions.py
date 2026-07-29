from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthenticatedOrReadOnly(BasePermission):
    """
    Lecture (GET/HEAD/OPTIONS) : ouverte a tous, connectes ou non.
    Ecriture (POST/PUT/PATCH/DELETE) : reservee aux utilisateurs authentifies.
    Utilisee pour TravelWish (via IsAuthenticated directement dans le
    ViewSet) et comme base conceptuelle pour Destination ci-dessous.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)


class DestinationPermission(BasePermission):
    """
    Regle specifique aux destinations (modification 3) :
      - Lecture (GET/HEAD/OPTIONS)      : ouverte a tous.
      - Creation/modification (POST,
        PUT, PATCH)                     : reservee aux utilisateurs authentifies.
      - Suppression (DELETE)            : reservee aux membres du staff
                                           (is_staff=True). Un utilisateur
                                           authentifie non-staff peut donc
                                           creer et modifier une destination,
                                           mais pas la supprimer.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if not (request.user and request.user.is_authenticated):
            return False

        if request.method == "DELETE":
            return bool(request.user.is_staff)

        # POST, PUT, PATCH : authentifie suffit, pas besoin d'etre staff
        return True
