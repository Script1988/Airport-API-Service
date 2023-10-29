from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from airport.models import Crew, Airport, Route, AirplaneType, Airplane, Flight
from airport.serializers import (
    CrewSerializer,
    AirportSerializer,
    RouteListSerializer,
    RouteDetailSerializer,
    AirplaneTypeSerializer,
    AirplaneListSerializer,
    FlightListSerializer,
    FlightDetailSerializer,
)

CREW_URL = reverse("airport:crew-list")
AIRPORT_URL = reverse("airport:airport-list")
ROUTE_URL = reverse("airport:route-list")
AIRPLANE_TYPE_URL = reverse("airport:airplane_type-list")
AIRPLANE_URL = reverse("airport:airplane-list")
FLIGHT_URL = reverse("airport:flight-list")


def sample_crew(**params):
    default = {
        "first_name": "Test name",
        "last_name": "Last name"
    }

    default.update(params)
    return Crew.objects.create(**default)


def sample_airport(**params):
    default = {
        "name": "Test airport",
        "closest_big_city": "London"
    }

    default.update(params)
    return Airport.objects.create(**default)


def sample_route(**params):
    source = sample_airport()
    destination = sample_airport()
    default = {
        "source": source,
        "destination": destination,
        "distance": 2000,
    }

    default.update(params)
    return Route.objects.create(**default)


def sample_airplane_type(**params):
    default = {
        "name": "Test airplane type",
    }

    default.update(params)
    return AirplaneType.objects.create(**default)


def sample_airplane(**params):
    airplane_type = sample_airplane_type()
    default = {
        "name": "Test airplane",
        "rows": 50,
        "seats_in_row": 6,
        "airplane_type": airplane_type
    }

    default.update(params)
    return Airplane.objects.create(**default)


def sample_flight(**params):
    route = sample_route()
    airplane = sample_airplane()
    default = {
        "route": route,
        "airplane": airplane,
        "departure_time": "2023-10-17",
        "arrival_time": "2023-10-18",
    }

    default.update(params)
    return Flight.objects.create(**default)


class UnauthenticatedMovieApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(FLIGHT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAirportApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@admin.com",
            password="testpass",
            is_staff=False,
        )
        self.client.force_authenticate(self.user)

    def test_create_crew_forbidden(self):
        payload = {
            "first_name": "John",
            "last_name": "Brzenk",
        }
        result = self.client.post(CREW_URL, payload)
        self.assertEqual(result.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_airport_forbidden(self):
        payload = {
            "name": "Test",
            "closest_big_city": "Test city",
        }
        result = self.client.post(AIRPORT_URL, payload)
        self.assertEqual(result.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_airplane_type_forbidden(self):
        payload = {
            "name": "Test AirplaneType",
        }
        result = self.client.post(AIRPLANE_TYPE_URL, payload)
        self.assertEqual(result.status_code, status.HTTP_403_FORBIDDEN)

    def test_crew_list(self):
        result = self.client.get(CREW_URL)
        crew = Crew.objects.all()
        serializer = CrewSerializer(crew, many=True)
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.data, serializer.data)

    def test_airport_list(self):
        result = self.client.get(AIRPORT_URL)
        airport = Airport.objects.all()
        serializer = AirportSerializer(airport, many=True)
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.data, serializer.data)

    def test_route_list(self):
        result = self.client.get(ROUTE_URL)
        route = Route.objects.all()
        serializer = RouteListSerializer(route, many=True)
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.data, serializer.data)

    def test_route_detail(self):
        test_route = sample_route()

        route_detail_url = f"{ROUTE_URL}{test_route.id}/"

        result = self.client.get(route_detail_url)

        serializer = RouteDetailSerializer(test_route)

        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.data, serializer.data)

    def test_airplane_type_list(self):
        result = self.client.get(AIRPLANE_TYPE_URL)
        airplane_type = AirplaneType.objects.all()
        serializer = AirplaneTypeSerializer(airplane_type, many=True)
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.data, serializer.data)

    def test_airplane_list(self):
        result = self.client.get(AIRPLANE_URL)
        airplane = Airplane.objects.all()
        serializer = AirplaneListSerializer(airplane, many=True)
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.data, serializer.data)

    def test_flight_list(self):
        result = self.client.get(FLIGHT_URL)
        flight = Flight.objects.all()
        serializer = FlightListSerializer(flight, many=True)
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.data, serializer.data)

    def test_flight_detail(self):
        test_flight = sample_flight()

        flight_detail_url = f"{FLIGHT_URL}{test_flight.id}/"

        result = self.client.get(flight_detail_url)
        result.data["departure_time"] = result.data["departure_time"].split("T00")[0]
        result.data["arrival_time"] = result.data["arrival_time"].split("T00")[0]

        serializer = FlightDetailSerializer(test_flight)

        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.data, serializer.data)


class AdminApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@admin.com",
            password="testpass",
            is_staff=True,
        )
        self.client.force_authenticate(self.user)

    def test_create_crew_allowed(self):
        payload = {
            "first_name": "John",
            "last_name": "Brzenk",
        }
        result = self.client.post(CREW_URL, payload)
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    def test_create_airport_allowed(self):
        payload = {
            "name": "Test",
            "closest_big_city": "Test city",
        }
        result = self.client.post(AIRPORT_URL, payload)
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    def test_create_airplane_type_allowed(self):
        payload = {
            "name": "Test AirplaneType",
        }
        result = self.client.post(AIRPLANE_TYPE_URL, payload)
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    # def test_create_airplane_allowed(self):
    #     airplane_type = sample_airplane_type()
    #     payload = {
    #         "name": "Test Airplane",
    #         "rows": 50,
    #         "seats_in_row": 6,
    #         "airplane_type": airplane_type.id,
    #     }
    #     result = self.client.post(AIRPLANE_URL, payload)
    #     self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    # def test_create_route_allowed(self):
    #     source = sample_airport()
    #     destination = sample_airport(name="Paris", closest_big_city="Paris")
    #     payload = {
    #         "source": source.id,
    #         "destination": destination.id,
    #         "distance": 3000,
    #     }
    #
    #     result = self.client.post(ROUTE_URL, payload)
    #
    #     self.assertEqual(result.status_code, status.HTTP_201_CREATED)

 # def test_create_movie(self):
 #        actor = Actor.objects.create(first_name="Test", last_name="Try")
 #        genre = Genre.objects.create(name="Genre")
 #        payload = {
 #            "title": "Test",
 #            "description": "Test",
 #            "duration": 120,
 #            "actors": actor.id,
 #            "genres": genre.id,
 #        }
 #        res = self.client.post(MOVIE_URL, payload)
 #
 #        self.assertEqual(res.status_code, status.HTTP_201_CREATED)