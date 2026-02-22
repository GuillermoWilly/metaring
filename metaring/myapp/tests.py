from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Airports

User = get_user_model()


# ===============================
# MODEL TESTS
# ===============================

class AirportModelTest(TestCase):

    def setUp(self):
        self.airport = Airports.objects.create(
            icao="LEMD",
            iata="MAD",
            name="Madrid Barajas International Airport",
            city="Madrid",
            subd="Comunidad de Madrid",
            country="ES",
            elevation="2001",
            lat="40.4936",
            lon="-3.56676",
            tz="Europe/Madrid",
            lid=""
        )

    def test_airport_creation(self):
        self.assertEqual(self.airport.icao, "LEMD")
        self.assertEqual(self.airport.name, "Madrid Barajas International Airport")

    def test_str_method(self):
        self.assertEqual(
            str(self.airport),
            "LEMD - Madrid Barajas International Airport"
    )


# ===============================
# VIEW TESTS
# ===============================

class HomeViewTest(TestCase):

    def test_home_page_status(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_home_template_used(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "home.html")


class AirportDetailViewTest(TestCase):

    def setUp(self):
        self.airport = Airports.objects.create(
            icao="LEMD",
            iata="MAD",
            name="Madrid Barajas International Airport",
            city="Madrid",
            subd="Comunidad de Madrid",
            country="ES",
            elevation="2001",
            lat="40.4936",
            lon="-3.56676",
            tz="Europe/Madrid",
            lid=""
        )

    def test_airport_detail_status(self):
        response = self.client.get(reverse("airport_detail", args=["LEMD"]))
        self.assertEqual(response.status_code, 200)

    def test_airport_detail_context(self):
        response = self.client.get(reverse("airport_detail", args=["LEMD"]))
        self.assertEqual(response.context["airport"].icao, "LEMD")


# ===============================
# AUTH TESTS
# ===============================

class AuthTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123"
        )

    def test_login(self):
        login = self.client.login(
            username="testuser",
            password="testpassword123"
        )
        self.assertTrue(login)

    def test_register_view(self):
        response = self.client.post(reverse("register"), {
            "username": "newuser",
            "password1": "StrongPassword123",
            "password2": "StrongPassword123"
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success


# ===============================
# FAVORITES TEST
# ===============================

class FavoriteTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="pilot",
            password="test12345"
        )

        self.airport = Airports.objects.create(
            icao="LEBL",
            iata="BCN",
            name="Barcelona International Airport",
            city="Barcelona",
            subd="Cataluña",
            country="ES",
            elevation="12",
            lat="41.2971",
            lon="2.07846",
            tz="Europe/Madrid",
            lid=""
        )

    def test_add_favorite(self):
        self.client.login(username="pilot", password="test12345")

        response = self.client.post(
            reverse("toggle_favorite", args=["LEBL"])
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(self.user, self.airport.favorited_by.all())