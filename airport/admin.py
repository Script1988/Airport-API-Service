from django.contrib import admin

from airport.models import (
    Crew,
    Airport,
    Route,
    Flight,
    AirplaneType,
    Airplane,
)

admin.site.register(Crew)
admin.site.register(AirplaneType)
admin.site.register(Airplane)
admin.site.register(Airport)
admin.site.register(Route)
admin.site.register(Flight)
