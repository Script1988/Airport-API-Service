from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


from airport.models import Crew, Airport, Route, Flight, AirplaneType, Airplane
from airport.serializers import (
    CrewSerializer,
    AirportSerializer,
    RouteListSerializer,
    RouteDetailSerializer,
    AirplaneListSerializer,
    FlightListSerializer,
    FlightDetailSerializer,
    AirplaneTypeSerializer,
)

CREW_URL = reverse("airport:crew-list")
AIRPORT_URL = reverse("airport:airport-list")
ROUTE_URL = reverse("airport:route-list")
AIRPLANE_TYPE_URL = reverse("airport:airplane_type-list")
AIRPLANE_URL = reverse("airport:airplane-list")
FLIGHT_URL = reverse("airport:flight-list")


def sample_crew(**params) -> Crew:
    default = {
        "first_name": "Test name",
        "last_name": "Last name"
    }

    default.update(params)
    return Crew.objects.create(**default)


def sample_airport(**params) -> Airport:
    default = {
        "name": "Test airport",
        "closest_big_city": "London"
    }

    default.update(params)
    return Airport.objects.create(**default)


def sample_route(**params) -> Route:
    source = sample_airport()
    destination = sample_airport()
    default = {
        "source": source,
        "destination": destination,
        "distance": 2000,
    }

    default.update(params)
    return Route.objects.create(**default)


def sample_airplane_type(**params) -> AirplaneType:
    default = {
        "name": "Test airplane type",
    }

    default.update(params)
    return AirplaneType.objects.create(**default)


def sample_airplane(**params) -> Airplane:
    airplane_type = sample_airplane_type()
    default = {
        "name": "Test airplane",
        "rows": 50,
        "seats_in_row": 6,
        "airplane_type": airplane_type
    }

    default.update(params)
    return Airplane.objects.create(**default)


def sample_flight(**params) -> Flight:
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

    def test_auth_required(self) -> None:
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

    def test_create_crew_forbidden(self) -> None:
        payload = {
            "first_name": "John",
            "last_name": "Brzenk",
        }
        result = self.client.post(CREW_URL, payload)
        self.assertEqual(result.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_airport_forbidden(self) -> None:
        payload = {
            "name": "Test",
            "closest_big_city": "Test city",
        }
        result = self.client.post(AIRPORT_URL, payload)
        self.assertEqual(result.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_airplane_type_forbidden(self) -> None:
        payload = {
            "name": "Test AirplaneType",
        }
        result = self.client.post(AIRPLANE_TYPE_URL, payload)
        self.assertEqual(result.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_route_forbidden(self) -> None:
        source = sample_airport()
        destination = sample_airport(name="Paris", closest_big_city="Paris")
        payload = {
            "source": source.id,
            "destination": destination.id,
            "distance": 3000,
        }

        result = self.client.post(ROUTE_URL, payload)

        self.assertEqual(result.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_airplane_forbidden(self) -> None:
        airplane_type = sample_airplane_type()
        payload = {
            "name": "Test Airplane",
            "rows": 50,
            "seats_in_row": 6,
            "airplane_type": airplane_type.id,
        }
        result = self.client.post(AIRPLANE_URL, payload)
        self.assertEqual(result.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_flight_forbidden(self) -> None:
        route = sample_route()
        crew = sample_crew()
        airplane = sample_airplane()
        payload = {
            "route": route.id,
            "airplane": airplane.id,
            "departure_time": "2023-10-21",
            "arrival_time": "2023-10-22",
            "crew": crew.id,
        }

        result = self.client.post(FLIGHT_URL, payload)
        self.assertEqual(result.status_code, status.HTTP_403_FORBIDDEN)

    def test_crew_list(self) -> None:
        result = self.client.get(CREW_URL)
        crew = Crew.objects.all()
        serializer = CrewSerializer(crew, many=True)
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.data, serializer.data)

    def test_airport_list(self) -> None:
        result = self.client.get(AIRPORT_URL)
        airport = Airport.objects.all()
        serializer = AirportSerializer(airport, many=True)
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.data, serializer.data)

    def test_route_list(self) -> None:
        result = self.client.get(ROUTE_URL)
        route = Route.objects.all()
        serializer = RouteListSerializer(route, many=True)
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.data, serializer.data)

    def test_route_detail(self) -> None:
        test_route = sample_route()

        route_detail_url = f"{ROUTE_URL}{test_route.id}/"

        result = self.client.get(route_detail_url)

        serializer = RouteDetailSerializer(test_route)

        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.data, serializer.data)

    def test_airplane_type_list(self) -> None:
        result = self.client.get(AIRPLANE_TYPE_URL)
        airplane_type = AirplaneType.objects.all()
        serializer = AirplaneTypeSerializer(airplane_type, many=True)
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.data, serializer.data)

    def test_airplane_list(self) -> None:
        result = self.client.get(AIRPLANE_URL)
        airplane = Airplane.objects.all()
        serializer = AirplaneListSerializer(airplane, many=True)
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.data, serializer.data)

    def test_flight_list(self) -> None:
        result = self.client.get(FLIGHT_URL)
        flight = Flight.objects.all()
        serializer = FlightListSerializer(flight, many=True)
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.data, serializer.data)

    def test_flight_detail(self) -> None:
        test_flight = sample_flight()

        flight_detail_url = f"{FLIGHT_URL}{test_flight.id}/"

        result = self.client.get(flight_detail_url)
        result.data["departure_time"] = result.data["departure_time"].split("T00")[0]
        result.data["arrival_time"] = result.data["arrival_time"].split("T00")[0]

        serializer = FlightDetailSerializer(test_flight)

        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.data, serializer.data)

    def test_filter_flight_by_source_airport(self) -> None:
        airport = Airport.objects.create(name="Borispol", closest_big_city="Kyiv")
        route = sample_route(source=airport)

        flight1 = sample_flight(route=route)
        flight2 = sample_flight()
        flight3 = sample_flight()

        queryset_url = f"{FLIGHT_URL}?source_airport={flight1.route.source.name}"
        result = self.client.get(queryset_url)
        result_data = [(key, value) for key, value in result.data[0].items()]
        response_data = {k[0]: k[1] for k in result_data}

        serializer1 = FlightListSerializer(flight1)
        serializer2 = FlightListSerializer(flight2)
        serializer3 = FlightListSerializer(flight3)

        self.assertIn(serializer1.data["source"], response_data["source"])
        self.assertNotIn(serializer2.data["source"], response_data["source"])
        self.assertNotIn(serializer3.data["source"], response_data["source"])

    def test_filter_flight_by_destination_airport(self) -> None:
        airport = Airport.objects.create(name="Heathrow", closest_big_city="London")
        route = sample_route(destination=airport)

        flight1 = sample_flight(route=route)
        flight2 = sample_flight()
        flight3 = sample_flight()

        queryset_url = f"{FLIGHT_URL}?destination_airport={flight1.route.destination.name}"
        result = self.client.get(queryset_url)
        result_data = [(key, value) for key, value in result.data[0].items()]
        response_data = {k[0]: k[1] for k in result_data}

        serializer1 = FlightListSerializer(flight1)
        serializer2 = FlightListSerializer(flight2)
        serializer3 = FlightListSerializer(flight3)

        self.assertIn(serializer1.data["destination"], response_data["destination"])
        self.assertNotIn(serializer2.data["destination"], response_data["destination"])
        self.assertNotIn(serializer3.data["destination"], response_data["destination"])

    def test_filter_flight_by_departure_time(self) -> None:
        flight1 = sample_flight()
        flight2 = sample_flight(departure_time="2023-10-20")
        flight3 = sample_flight(departure_time="2023-10-21")

        queryset_url = f"{FLIGHT_URL}?departure_time={flight1.departure_time}"
        result = self.client.get(queryset_url)

        serializer1 = FlightListSerializer(flight1)
        serializer2 = FlightListSerializer(flight2)
        serializer3 = FlightListSerializer(flight3)
        result_data = [(key, value) for key, value in result.data[0].items()]
        response_data = {k[0]: k[1] for k in result_data}
        data_to_check = response_data["departure_time"].split("T00")[0]

        self.assertIn(serializer1.data["departure_time"], data_to_check)
        self.assertNotIn(serializer2.data["departure_time"], data_to_check)
        self.assertNotIn(serializer3.data["departure_time"], data_to_check)


class AdminApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@admin.com",
            password="testpass",
            is_staff=True,
        )
        self.client.force_authenticate(self.user)

    def test_create_crew_allowed(self) -> None:
        payload = {
            "first_name": "John",
            "last_name": "Brzenk",
        }
        result = self.client.post(CREW_URL, payload)
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    def test_create_airport_allowed(self) -> None:
        payload = {
            "name": "Test",
            "closest_big_city": "Test city",
        }
        result = self.client.post(AIRPORT_URL, payload)
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    def test_create_airplane_type_allowed(self) -> None:
        payload = {
            "name": "Test AirplaneType",
        }
        result = self.client.post(AIRPLANE_TYPE_URL, payload)
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    def test_create_route_allowed(self) -> None:
        source = sample_airport()
        destination = sample_airport(name="Paris", closest_big_city="Paris")
        payload = {
            "source": source.id,
            "destination": destination.id,
            "distance": 3000,
        }

        result = self.client.post(ROUTE_URL, payload)

        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    def test_create_airplane_allowed(self) -> None:
        airplane_type = sample_airplane_type()
        payload = {
            "name": "Test Airplane",
            "rows": 50,
            "seats_in_row": 6,
            "airplane_type": airplane_type.id,
        }
        result = self.client.post(AIRPLANE_URL, payload)
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    def test_create_flight_allowed(self) -> None:
        route = sample_route()
        crew = sample_crew()
        airplane = sample_airplane()
        payload = {
            "route": route.id,
            "airplane": airplane.id,
            "departure_time": "2023-10-21",
            "arrival_time": "2023-10-22",
            "crew": crew.id,
        }

        result = self.client.post(FLIGHT_URL, payload)
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
