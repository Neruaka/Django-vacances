from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from decimal import Decimal
from django.contrib.auth.models import User
from travel.models import TravelWish,Destination

class DestinationAPITestCase(APITestCase):
    def setUp(self):
        """Données créées avant chaque test."""

        self.user = User.objects.create_user(
            username="user",
            email="",
            password="test1234",
        )

        self.destination = Destination.objects.create(
            city = "Victoria Falls",
            country = "Zimbabwe",
            continent = "Afrique",
            description = "Destination connue pour les célèbres chutes Victoria.",
            best_period = "Février à mai",
            average_budget = Decimal("1800.00"),
        )

        self.travel_wish = TravelWish.objects.create(
            user=self.user,
            destination=self.destination,
            priority="high",
            desired_period="Printemps 2027",
            notes="À faire pendant les périodes de paques",
            visited=False,
        )

    def test_get_destination_list(self):
        url = reverse("travel:destination-list")

        response = self.client.get(url)
        print("Test : test_get_destination_list")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(len(response.data["results"]), 1)

        self.assertEqual(
            response.data["results"][0]["city"],
            "Victoria Falls",
        )
        self.assertEqual(
            response.data["results"][0]["country"],
            "Zimbabwe",
        )
        self.assertEqual(
            response.data["results"][0]["continent"],
            "Afrique",
        )
        self.assertEqual(
            response.data["results"][0]["description"],
            "Destination connue pour les célèbres chutes Victoria.",
        )
        self.assertEqual(
            response.data["results"][0]["best_period"],
            "Février à mai",
        )
        self.assertEqual(
            response.data["results"][0]["average_budget"],
            "1800.00",
        )
    