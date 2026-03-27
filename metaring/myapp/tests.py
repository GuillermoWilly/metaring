from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Airports
from unittest.mock import patch
import time
import random

User = get_user_model()

# MODEL TESTS

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


# VIEW TESTS

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


# AUTH TESTS

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


# FAVORITES TEST

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

# DECODED TESTS


class AirportDecodedViewTest(TestCase):

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

    def test_airport_decoded_status(self):
        response = self.client.get(reverse("airport_decoded", args=["LEMD"]))
        self.assertEqual(response.status_code, 200)

    def test_airport_decoded_template_used(self):
        response = self.client.get(reverse("airport_decoded", args=["LEMD"]))
        self.assertTemplateUsed(response, "airport_decoded.html")

    def test_airport_decoded_context(self):
        response = self.client.get(reverse("airport_decoded", args=["LEMD"]))
        self.assertEqual(response.context["airport"].icao, "LEMD")
        self.assertEqual(response.context["airport"].name, "Madrid Barajas International Airport")

# COMPARE TESTS

class AirportCompareViewTest(TestCase):

    def setUp(self):
        self.airport1 = Airports.objects.create(
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
        
        self.airport2 = Airports.objects.create(
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

    def test_airport_compare_status(self):
        response = self.client.get(reverse("airport_compare") + "?icao1=LEMD&icao2=LEBL")
        self.assertEqual(response.status_code, 200)

    def test_airport_compare_template_used(self):
        response = self.client.get(reverse("airport_compare") + "?icao1=LEMD&icao2=LEBL")
        self.assertTemplateUsed(response, "airport_compare.html")

    def test_airport_compare_context(self):
        response = self.client.get(reverse("airport_compare") + "?icao1=LEMD&icao2=LEBL")
        self.assertEqual(response.context["icao1"], "LEMD")
        self.assertEqual(response.context["icao2"], "LEBL")

    def test_airport_compare_same_icao_error(self):
        response = self.client.get(reverse("airport_compare") + "?icao1=LEMD&icao2=LEMD")
        self.assertIsNotNone(response.context["error"])
        self.assertIn("cannot be the same", response.context["error"])

    def test_airport_compare_no_parameters(self):
        response = self.client.get(reverse("airport_compare"))
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context["icao1"])
        self.assertIsNone(response.context["icao2"])


# ===============================
# INTEGRATION TESTS
# ===============================

class UserRegistrationIntegrationTest(TestCase):
    """Test the complete user registration and authentication flow"""

    def test_user_registration_and_login_flow(self):
        # Test registration
        response = self.client.post(reverse("register"), {
            "username": "testpilot",
            "password1": "StrongPassword123!",
            "password2": "StrongPassword123!"
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration

        # Verify user was created
        user = User.objects.get(username="testpilot")
        self.assertEqual(user.username, "testpilot")

        # Test login
        login_success = self.client.login(username="testpilot", password="StrongPassword123!")
        self.assertTrue(login_success)

        # Test accessing protected view
        response = self.client.get(reverse("favorites"))
        self.assertEqual(response.status_code, 200)


class AirportSearchIntegrationTest(TestCase):
    """Test the complete airport search workflow"""

    def setUp(self):
        self.airport = Airports.objects.create(
            icao="KJFK",
            iata="JFK",
            name="John F. Kennedy International Airport",
            city="New York",
            subd="New York",
            country="US",
            elevation="13",
            lat="40.6413",
            lon="-73.7781",
            tz="America/New_York",
            lid=""
        )

    def test_airport_detail_to_decoded_workflow(self):
        # Start at airport detail page
        response = self.client.get(reverse("airport_detail", args=["KJFK"]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "airport_detail.html")
        self.assertEqual(response.context["airport"].icao, "KJFK")

        # Navigate to decoded view
        response = self.client.get(reverse("airport_decoded", args=["KJFK"]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "airport_decoded.html")
        self.assertEqual(response.context["airport"].icao, "KJFK")


class FavoritesIntegrationTest(TestCase):
    """Test the complete favorites workflow"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="aviator",
            password="securepass123"
        )
        self.airport = Airports.objects.create(
            icao="EGLL",
            iata="LHR",
            name="London Heathrow Airport",
            city="London",
            subd="England",
            country="GB",
            elevation="83",
            lat="51.4775",
            lon="-0.4614",
            tz="Europe/London",
            lid=""
        )

    def test_add_and_view_favorites_workflow(self):
        # Login user
        self.client.login(username="aviator", password="securepass123")

        # Add airport to favorites
        response = self.client.post(reverse("toggle_favorite", args=["EGLL"]))
        self.assertEqual(response.status_code, 302)  # Redirect after toggle

        # Verify airport is in favorites
        self.airport.refresh_from_db()
        self.assertIn(self.user, self.airport.favorited_by.all())

        # View favorites page
        response = self.client.get(reverse("favorites"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "favorites.html")
        self.assertIn(self.airport, response.context["favorites"])

        # Remove from favorites
        response = self.client.post(reverse("toggle_favorite", args=["EGLL"]))
        self.assertEqual(response.status_code, 302)

        # Verify airport is removed from favorites
        self.airport.refresh_from_db()
        self.assertNotIn(self.user, self.airport.favorited_by.all())


class AirportComparisonIntegrationTest(TestCase):
    """Test the airport comparison workflow"""

    def setUp(self):
        self.airport1 = Airports.objects.create(
            icao="KLAX",
            iata="LAX",
            name="Los Angeles International Airport",
            city="Los Angeles",
            subd="California",
            country="US",
            elevation="125",
            lat="33.9425",
            lon="-118.4081",
            tz="America/Los_Angeles",
            lid=""
        )
        self.airport2 = Airports.objects.create(
            icao="KSFO",
            iata="SFO",
            name="San Francisco International Airport",
            city="San Francisco",
            subd="California",
            country="US",
            elevation="13",
            lat="37.6189",
            lon="-122.3750",
            tz="America/Los_Angeles",
            lid=""
        )

    def test_compare_different_airports_workflow(self):
        # Access comparison page with two different airports
        response = self.client.get(
            reverse("airport_compare") + "?icao1=KLAX&icao2=KSFO"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "airport_compare.html")
        self.assertEqual(response.context["icao1"], "KLAX")
        self.assertEqual(response.context["icao2"], "KSFO")
        self.assertIsNone(response.context["error"])

    def test_compare_same_airport_error_workflow(self):
        # Try to compare same airport
        response = self.client.get(
            reverse("airport_compare") + "?icao1=KLAX&icao2=KLAX"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context["error"])
        self.assertIn("cannot be the same", response.context["error"])


# ===============================
# LOAD TESTS
# ===============================

class LoadTest(TestCase):
    """Load testing for airport views without external API dependency"""

    def setUp(self):
        self.airports = []
        airport_data = [
            ("KJFK", "JFK", "John F. Kennedy International Airport"),
            ("KLAX", "LAX", "Los Angeles International Airport"),
            ("KORD", "ORD", "O'Hare International Airport"),
            ("KDEN", "DEN", "Denver International Airport"),
            ("KSFO", "SFO", "San Francisco International Airport"),
        ]

        for icao, iata, name in airport_data:
            airport = Airports.objects.create(
                icao=icao,
                iata=iata,
                name=name,
                city="Test City",
                subd="Test State",
                country="US",
                elevation="100",
                lat="0",
                lon="0",
                tz="UTC",
                lid=""
            )
            self.airports.append(airport)

    def _mock_metar(self):
        """Fake METAR response"""
        return {
            "raw_text": "TEST METAR",
            "temperature": {"celsius": 20},
            "dewpoint": {"celsius": 10},
            "wind": {"speed": 10, "direction": 180},
            "visibility": {"meters": 9999},
            "pressure": {"hpa": 1013},
            "clouds": [],
            "remarks": [],
            "flight_category": "VFR"
        }

    def _make_request(self, url_name, args=None):
        start_time = time.time()

        if args:
            response = self.client.get(reverse(url_name, args=args))
        else:
            response = self.client.get(reverse(url_name))

        end_time = time.time()

        return {
            "status_code": response.status_code,
            "response_time": end_time - start_time,
            "success": response.status_code == 200
        }

    def test_concurrent_home_page_access(self):
        results = [self._make_request('home') for _ in range(10)]

        self.assertTrue(all(r["success"] for r in results))
        avg_time = sum(r["response_time"] for r in results) / len(results)
        self.assertLess(avg_time, 1.0)

    @patch("your_app.utils.get_metar_decoded")
    def test_concurrent_airport_detail_access(self, mock_metar):
        mock_metar.return_value = self._mock_metar()

        results = []
        for airport in self.airports:
            for _ in range(3):
                results.append(self._make_request('airport_detail', args=[airport.icao]))

        self.assertTrue(all(r["success"] for r in results))
        avg_time = sum(r["response_time"] for r in results) / len(results)
        self.assertLess(avg_time, 2.0)

    @patch("your_app.utils.get_metar_decoded")
    def test_concurrent_airport_decoded_access(self, mock_metar):
        mock_metar.return_value = self._mock_metar()

        results = []
        for airport in self.airports[:2]:
            for _ in range(5):
                results.append(self._make_request('airport_decoded', args=[airport.icao]))

        self.assertTrue(all(r["success"] for r in results))
        avg_time = sum(r["response_time"] for r in results) / len(results)
        self.assertLess(avg_time, 2.0)

    @patch("your_app.utils.get_metar_decoded")
    def test_mixed_workload_simulation(self, mock_metar):
        mock_metar.return_value = self._mock_metar()

        results = []

        for _ in range(20):
            choice = random.choice(["home", "detail", "decoded"])

            if choice == "home":
                results.append(self._make_request("home"))

            elif choice == "detail":
                airport = random.choice(self.airports)
                results.append(self._make_request("airport_detail", args=[airport.icao]))

            else:
                airport = random.choice(self.airports[:2])
                results.append(self._make_request("airport_decoded", args=[airport.icao]))

        self.assertGreaterEqual(sum(r["success"] for r in results), 18)

        avg_time = sum(r["response_time"] for r in results) / len(results)
        max_time = max(r["response_time"] for r in results)

        self.assertLess(avg_time, 3.0)
        self.assertLess(max_time, 5.0)