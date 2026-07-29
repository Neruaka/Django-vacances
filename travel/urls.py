from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .api_views import DestinationViewSet, TravelWishViewSet

router = DefaultRouter()
router.register("destinations", DestinationViewSet, basename="destination")
router.register("wishes", TravelWishViewSet, basename="travel-wish")

app_name = "travel"

urlpatterns = [
    # Pages HTML classiques (cahier des charges point 7 + modifications 1 et 4)
    path("destinations/", views.destination_list, name="destination_list"),
    path("destinations/<int:pk>/", views.destination_detail, name="destination_detail"),
    path("wishes/", views.wish_list, name="wish_list"),
    path("wishes/<int:pk>/", views.wish_detail, name="wish_detail"),

    # Routes API generees automatiquement par le router (point 3), toutes
    # prefixees par "api/" pour ne jamais entrer en collision avec les
    # routes HTML ci-dessus.
    path("api/", include(router.urls)),
]
