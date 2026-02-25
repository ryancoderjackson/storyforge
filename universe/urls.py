from django.urls import path
from .views import timeline_home, event_detail, factions_index, faction_detail, locations_index, location_detail

app_name = "universe"

urlpatterns = [
    path("", timeline_home, name="timeline_home"),
    path("events/<int:pk>/", event_detail, name="event_detail"),
    path("factions/", factions_index, name="factions_index"),
    path("factions/<int:pk>/", faction_detail, name="faction_detail"),
    path("locations/", locations_index, name="locations_index"),
    path("locations/<int:pk>/", location_detail, name="location_detail"),
]