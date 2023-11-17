from django.db import models
from airport.utils import crew_image_file_path


class Crew(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    image = models.ImageField(null=True, upload_to=crew_image_file_path)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Airport(models.Model):
    name = models.CharField(max_length=255)
    closest_big_city = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return self.name


class Route(models.Model):
    source = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="route_source")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="route_destination")
    distance = models.IntegerField(default=2000)

    def __str__(self) -> str:
        return f"Fly from {self.source} to {self.destination}. Distance: {self.distance}"


class AirplaneType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Airplane(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplane_type = models.ForeignKey(AirplaneType, on_delete=models.CASCADE, related_name="airplane")

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self) -> str:
        return f"Airplane type: {self.airplane_type}. Total places: {self.capacity}"


class Flight(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="flight")
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE, related_name="flight")
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField(Crew, related_name="flight")

    def __str__(self) -> str:
        return f"Flight {self.route}. Departure: {self.departure_time}. Arrival: {self.arrival_time}"

    class Meta:
        ordering = ["departure_time"]
