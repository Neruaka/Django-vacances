"""
URL principal du projet. Ce fichier reste volontairement "chef d'orchestre" :
il delegue tout le detail des routes de l'app 'travel' via include(), et
n'ajoute que les routes globales (admin, authentification JWT, accueil).
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from wanderlist.travel import views as travel_views

urlpatterns = [
    # Page d'accueil (modification 4)
    path("", travel_views.home, name="home"),

    path("admin/", admin.site.urls),

    # Obtention du jeton JWT (cahier des charges, point 6) :
    # POST {"username": "...", "password": "..."} -> {"access": "...", "refresh": "..."}
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # Permet de renouveler un access token expire a partir du refresh token,
    # sans redemander le mot de passe.
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Toutes les autres routes de l'app travel (API + pages HTML) sont
    # prefixees ici.
    path("", include("travel.urls")),
]
