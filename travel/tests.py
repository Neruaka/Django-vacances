from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from decimal import Decimal
from django.contrib.auth.models import User
from travel.models import TravelWish,Destination
from rest_framework_simplejwt.tokens import AccessToken,RefreshToken

class DestinationAPITestCase(APITestCase):
    def setUp(self):
        """Données créées avant chaque test."""

        self.user = User.objects.create_user(
            username="user",
            email="",
            password="test1234",
        )
        self.staff_user = User.objects.create_user(
            username = "user_staff",
            email = "",
            password = "test1234",
            is_staff = True

        )

        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        refresh = RefreshToken.for_user(self.staff_user)
        self.staff_token = str(refresh.access_token)

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

    def test_get_destination_detail(self):
        url = reverse(
            "travel:destination-detail",
            kwargs={"pk": self.destination.pk},
        )

        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
             response.data["city"],
            "Victoria Falls",
        )

    def test_create_destination_with_basic_user(self):
        url = reverse("travel:destination-list")
        data = {
            "city": "Rome",
            "country": "Italie",
            "continent": "europe",
            "description": "Ville historique connue pour le Colisée, le Vatican et sa cuisine.",
            "best_period": "Avril à juin et septembre à octobre",
            "average_budget": 1100.00
        }

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

        response = self.client.post(
                    url,
                    data,
                    format="json",
                )
        
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(Destination.objects.count(), 2)
        self.assertTrue(
            Destination.objects.filter(
                city="Rome",
                country="Italie",
            ).exists()
        )

    def test_create_destination_with_staff_user(self):
        url = reverse("travel:destination-list")
        data = {
            "city": "Rome",
            "country": "Italie",
            "continent": "europe",
            "description": "Ville historique connue pour le Colisée, le Vatican et sa cuisine.",
            "best_period": "Avril à juin et septembre à octobre",
            "average_budget": 1100.00
        }

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}"
        )

        response = self.client.post(
                    url,
                    data,
                    format="json",
                )
        
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(Destination.objects.count(), 2)
        self.assertTrue(
            Destination.objects.filter(
                city="Rome",
                country="Italie",
            ).exists()
        )

    def test_create_destination_with_user_not_authenticated(self):
        url = reverse("travel:destination-list")
        data = {
            "city": "Rome",
            "country": "Italie",
            "continent": "europe",
            "description": "Ville historique connue pour le Colisée, le Vatican et sa cuisine.",
            "best_period": "Avril à juin et septembre à octobre",
            "average_budget": 1100.00
        }

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer "
        )

        response = self.client.post(
                    url,
                    data,
                    format="json",
                )
        
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )



    def test_update_destination_with_basic_user(self):
        url = reverse(
            "travel:destination-detail",
            kwargs={"pk": self.destination.pk},
        )

        data = {
            "best_period": "Avril à juin",
        }
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        response = self.client.patch(
            url,
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_destination_with_staff_user(self):
        url = reverse(
            "travel:destination-detail",
            kwargs={"pk": self.destination.pk},
        )

        data = {
            "best_period": "Avril à juin",
        }
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}"
        )
        response = self.client.patch(
            url,
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.destination.refresh_from_db()

        self.assertEqual(self.destination.best_period,"Avril à juin")

    def test_update_destination_with_user_not_authenticated(self):
        url = reverse(
            "travel:destination-detail",
            kwargs={"pk": self.destination.pk},
        )

        data = {
            "best_period": "Avril à juin",
        }
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer "
        )
        response = self.client.patch(
            url,
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



    def test_delete_experiment_with_basic_user(self):
            url = reverse(
                "travel:destination-detail",
                kwargs={"pk": self.destination.pk},
            )
            self.client.credentials(
                HTTP_AUTHORIZATION=f"Bearer {self.token}"
            )
            response = self.client.delete(url)
    
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_delete_experiment_with_staff_user(self):
            url = reverse(
                "travel:destination-detail",
                kwargs={"pk": self.destination.pk},
            )
            self.client.credentials(
                HTTP_AUTHORIZATION=f"Bearer {self.staff_token}"
            )
            response = self.client.delete(url)
    
            self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
            )

            self.assertFalse(
            Destination.objects.filter(
                pk=self.destination.pk
            ).exists()
            )

    def test_delete_experiment_with_user_not_authenticated(self):
            url = reverse(
                "travel:destination-detail",
                kwargs={"pk": self.destination.pk},
            )
            self.client.credentials(
                HTTP_AUTHORIZATION=f"Bearer "
            )
            response = self.client.delete(url)
    
            self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            )
    