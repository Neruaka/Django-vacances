from django.conf import settings
from django.db import models


class Destination(models.Model):
    """
    Represente un lieu pouvant etre ajoute au carnet de voyage.
    Donnees publiques, gerees par l'equipe (staff).
    """

    CONTINENT_CHOICES = [
        ("africa", "Afrique"),
        ("america", "Amerique"),
        ("asia", "Asie"),
        ("europe", "Europe"),
        ("oceania", "Oceanie"),
    ]

    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    continent = models.CharField(max_length=20, choices=CONTINENT_CHOICES)
    description = models.TextField(blank=True)
    best_period = models.CharField(max_length=100, blank=True)
    average_budget = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["country", "city"]
        constraints = [
            models.UniqueConstraint(
                fields=["city", "country"],
                name="unique_destination_city_country",
            )
        ]

    def __str__(self) -> str:
        return f"{self.city}, {self.country}"


class TravelWish(models.Model):
    """
    Represente l'envie d'UN utilisateur precis de visiter UNE destination precise.
    Contient des informations personnelles (priorite, periode, notes) qu'un simple
    ManyToManyField ne pourrait pas stocker.
    """

    PRIORITY_CHOICES = [
        ("low", "Faible"),
        ("medium", "Moyenne"),
        ("high", "Haute"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="travel_wishes",
    )
    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        related_name="wishes",
    )
    priority = models.CharField(
        max_length=10, choices=PRIORITY_CHOICES, default="medium"
    )
    desired_period = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    visited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "destination"],
                name="unique_user_destination_wish",
            )
        ]

    def __str__(self) -> str:
        return f"{self.user.username} souhaite visiter {self.destination}"
