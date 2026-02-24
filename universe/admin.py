from django.contrib import admin
from .models import Universe, Faction, Location, Event

# Register your models here.
admin.site.register(Universe)
admin.site.register(Faction)
admin.site.register(Location)
admin.site.register(Event)