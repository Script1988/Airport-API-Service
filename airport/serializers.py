from rest_framework import serializers
from airport.models import Crew, Airport, Route, Flight, AirplaneType, Airplane


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "name", "closest_big_city")


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ("id", "name")


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = ("id", "name", "rows", "seats_in_row", "airplane_type")


class AirplaneListSerializer(AirplaneSerializer):
    airplane_type_name = serializers.CharField(source="airplane_type.name", read_only=True)

    class Meta:
        model = Airplane
        fields = (
            "id",
            "name",
            "rows",
            "seats_in_row",
            "airplane_type",
            "airplane_type_name",
            "capacity"
        )


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class RouteListSerializer(RouteSerializer):
    source_airport = serializers.CharField(source="source.name", read_only=True)
    destination_airport = serializers.CharField(source="destination.name", read_only=True)

    class Meta:
        model = Route
        fields = ("id",  "source_airport",  "destination_airport")


class RouteDetailSerializer(RouteSerializer):
    source = serializers.CharField(source="source.name", read_only=True)
    destination = serializers.CharField(source="destination.name", read_only=True)
    source_closest_big_city = serializers.CharField(source="source.closest_big_city", read_only=True)
    destination_closest_big_city = serializers.CharField(source="destination.closest_big_city", read_only=True)

    class Meta:
        model = Route
        fields = (
            "source",
            "source_closest_big_city",
            "destination",
            "destination_closest_big_city",
            "distance"
        )


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name", "image")


class CrewDetailSerializer(CrewSerializer):
    class Meta:
        model = Crew
        fields = ("first_name", "last_name", "image")


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ("id", "route", "airplane", "departure_time", "arrival_time", "crew")


class FlightListSerializer(FlightSerializer):
    source = serializers.CharField(source="route.source.name", read_only=True)
    destination = serializers.CharField(source="route.destination.name", read_only=True)
    tickets_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = Flight
        fields = (
            "id",
            "source",
            "destination",
            "departure_time",
            "arrival_time",
            "tickets_available"
        )


class FlightDetailSerializer(FlightListSerializer):
    crew = serializers.StringRelatedField(many=True)
    airplane = AirplaneListSerializer(many=False, read_only=True)
    source_closest_big_city = serializers.CharField(
        source="route.source.closest_big_city",
        read_only=True
    )
    destination_closest_big_city = serializers.CharField(
        source="route.destination.closest_big_city",
        read_only=True
    )

    class Meta:
        model = Flight
        fields = (
            "source",
            "source_closest_big_city",
            "destination",
            "destination_closest_big_city",
            "departure_time",
            "arrival_time",
            "crew",
            "airplane",
        )
