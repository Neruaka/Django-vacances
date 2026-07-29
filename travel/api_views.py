from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Destination, TravelWish
from .permissions import IsAuthenticatedOrReadOnly
from .serializers import DestinationSerializer, TravelWishSerializer


class DestinationViewSet(viewsets.ModelViewSet):
    """
    CRUD complet sur les destinations.
    Lecture publique, ecriture reservee aux utilisateurs authentifies
    (cahier des charges, point 5).
    """

    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class TravelWishViewSet(viewsets.ModelViewSet):
    """
    CRUD sur les envies de voyage. Chaque utilisateur ne voit et ne peut
    modifier QUE ses propres envies (get_queryset + perform_create).
    """

    serializer_class = TravelWishSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filtre systematique : un utilisateur ne recoit jamais les envies
        # d'un autre, y compris sur les routes de detail (GET .../15/).
        # Si l'objet 15 appartient a quelqu'un d'autre, il est absent de ce
        # queryset -> DRF repond 404, pas 403 (l'objet "n'existe pas" pour
        # cet utilisateur precis).
        return TravelWish.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Le champ 'user' est en read_only dans le serializer : le client ne
        # peut jamais l'envoyer. C'est ici, cote serveur, qu'on l'attribue
        # depuis l'utilisateur authentifie du token JWT. Empeche un
        # utilisateur de creer une envie au nom de quelqu'un d'autre.
        serializer.save(user=self.request.user)

    # Note : pas besoin de surcharger get_serializer_context() ici.
    # DRF y met deja automatiquement la requete ('request') par defaut,
    # c'est ce qui permet a TravelWishSerializer.validate() d'appeler
    # self.context.get("request") sans configuration supplementaire.

    @action(detail=True, methods=["post"], url_path="mark-visited")
    def mark_visited(self, request, pk=None):
        """
        Action personnalisee : POST /wishes/{id}/mark-visited/
        Marque une envie comme visitee. Reutilise get_object(), qui applique
        deja le filtrage de get_queryset() -> impossible de marquer comme
        visitee une envie appartenant a un autre utilisateur.
        """
        wish = self.get_object()
        wish.visited = True
        wish.save(update_fields=["visited"])
        serializer = self.get_serializer(wish)
        return Response(serializer.data, status=status.HTTP_200_OK)
