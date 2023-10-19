from django.db import models


class Crew(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Airport(models.Model):
    name = models.CharField(max_length=255)
    closest_big_city = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Airport name: {self.name}"


class Route(models.Model):
    source = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="route")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="route")
    distance = models.IntegerField()

    def __str__(self):
        return f"Fly from {self.source} to {self.destination}. Distance: {self.distance}"
