from django.conf import settings
from django.db import models

# Create your models here.
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Universe(TimeStampedModel):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="universes",
    )
    name = models.CharField(max_length=120)
    tagline = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Faction(TimeStampedModel):
    class Alignment(models.TextChoices):
        ORDER = "ORDER", "Order"
        CHAOS = "CHAOS", "Chaos"
        NEUTRAL = "NEUTRAL", "Neutral"
        UNKNOWN = "UNKNOWN", "Unknown"

    universe = models.ForeignKey(
        Universe,
        on_delete=models.CASCADE,
        related_name="factions",
    )
    name = models.CharField(max_length=120)
    short_name = models.CharField(max_length=60, blank=True)  # e.g., "Idols"
    description = models.TextField(blank=True)
    alignment = models.CharField(
        max_length=20,
        choices=Alignment.choices,
        default=Alignment.UNKNOWN,
    )

    def __str__(self):
        return f"{self.name} ({self.universe.name})"


class Location(TimeStampedModel):
    class LocationType(models.TextChoices):
        PLANET = "PLANET", "Planet"
        CITY = "CITY", "City"
        STATION = "STATION", "Station"
        REGION = "REGION", "Region"
        ORBIT = "ORBIT", "Orbit"
        OTHER = "OTHER", "Other"

    universe = models.ForeignKey(
        Universe,
        on_delete=models.CASCADE,
        related_name="locations",
    )
    name = models.CharField(max_length=120)
    location_type = models.CharField(
        max_length=20,
        choices=LocationType.choices,
        default=LocationType.OTHER,
    )
    description = models.TextField(blank=True)
    controlling_faction = models.ForeignKey(
        Faction,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="controlled_locations",
    )

    def __str__(self):
        return f"{self.name} ({self.universe.name})"


class Event(TimeStampedModel):
    class Era(models.IntegerChoices):
        BI = 0, "BI (Before Impact)"
        PI = 1, "PI (Post Impact)"

    class EventType(models.TextChoices):
        CATASTROPHE = "CATASTROPHE", "Catastrophe"
        DIPLOMACY = "DIPLOMACY", "Diplomacy"
        POLITICAL = "POLITICAL", "Political"
        SOCIAL = "SOCIAL", "Social"
        SCIENTIFIC = "SCIENTIFIC", "Scientific"
        MILITARY = "MILITARY", "Military"
        OTHER = "OTHER", "Other"

    universe = models.ForeignKey(
        Universe,
        on_delete=models.CASCADE,
        related_name="events",
    )
    title = models.CharField(max_length=160)
    summary = models.TextField(blank=True)

    era = models.IntegerField(choices=Era.choices, default=Era.PI)
    year = models.IntegerField(default=0)
    day = models.IntegerField(default=0)

    event_type = models.CharField(
        max_length=20,
        choices=EventType.choices,
        default=EventType.OTHER,
    )

    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="events",
    )

    factions = models.ManyToManyField(
        Faction,
        blank=True,
        related_name="events",
    )

    is_major = models.BooleanField(default=False)

    class Meta:
        ordering = ["era", "year", "day", "created_at"]

    def __str__(self):
        return f"{self.title} ({self.get_era_display()} {self.year} Day {self.day})"