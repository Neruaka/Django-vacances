from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from travel.models import Destination, TravelWish




class TravelWishModelTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="traveler",
            password="test1234",
        )

        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

        self.destination = Destination.objects.create(
            city="Tokyo",
            country="Japon",
            continent="asia",
        )

        self.destination_bis = Destination.objects.create(
            city="Paris",
            country="France",
            continent="Asia",
        )
        self.travel_wish = TravelWish.objects.create(
            user=self.user,
            destination=self.destination,
            priority="high",
            desired_period="Printemps 2027",
            notes="Voyage à organiser.",
            visited=False,
        )

    def test_travel_wish_creation(self):
        url = reverse("travel:travel-wish-list")
        data = {
            "destination" : self.destination_bis.pk,
            "priority" : "high",
            "desired_period" : "Ete 2027",
            "notes" : "Voyage à organiser.",
            "visited" : False
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

        self.assertTrue(
            TravelWish.objects.filter(
            user=self.user,
            destination=self.destination_bis,
        ).exists())

    def test_get_destination_list_user_not_authenticated(self):
        url = reverse("travel:travel-wish-list")
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer "
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_get_destination_list_with_user(self):
            url = reverse("travel:travel-wish-list")
            self.client.credentials(
                HTTP_AUTHORIZATION=f"Bearer {self.token}"
            )
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["count"], 1)
            self.assertEqual(len(response.data["results"]), 1)

    def test_update_destination_with_basic_user(self):
        url = reverse(
            "travel:travel-wish-detail",
            kwargs={"pk": self.destination.pk},
        )

        data = {
            "visited": True,
        }
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        response = self.client.patch(
            url,
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


def test_delete_wish_with_basic_user(self):
    url = reverse(
        "travel:travel-wish-detail",
        kwargs={"pk": self.destination.pk},
    )
    self.client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {self.token}"
    )
    response = self.client.delete(url)

    self.assertEqual(
    response.status_code,
    status.HTTP_204_NO_CONTENT,
    )

    self.assertFalse(
    TravelWish.objects.filter(
        pk=self.destination.pk
    ).exists()
    )

"""
    def test_default_priority_is_medium(self):
        destination = Destination.objects.create(
            city="Kyoto",
            country="Japon",
            continent="asia",
        )

        wish = TravelWish.objects.create(
            user=self.user,
            destination=destination,
        )

        self.assertEqual(wish.priority, "medium")
        self.assertFalse(wish.visited)

    def test_user_cannot_have_duplicate_wish(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                TravelWish.objects.create(
                    user=self.user,
                    destination=self.destination,
                )
"""