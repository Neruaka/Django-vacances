from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .api_views import DestinationViewSet, TravelWishViewSet

router = DefaultRouter()
router.register("destinations", DestinationViewSet, basename="destination")
router.register("wishes", TravelWishViewSet, basename="travel-wish")

app_name = "travel"

urlpatterns = [
    # Page HTML classique (point 7 du cahier des charges).
    # Chemin final : /destinations/
    path("destinations/", views.destination_list, name="destination_list"),

    # Routes API generees automatiquement par le router (point 3), toutes
    # prefixees par "api/" pour ne jamais entrer en collision avec la route
    # HTML ci-dessus (qui utilise aussi le mot "destinations").
    # Chemins finaux : /api/destinations/, /api/wishes/, etc.
    path("api/", include(router.urls)),
]
