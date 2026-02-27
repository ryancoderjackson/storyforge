from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch, Count, Q
from .models import Universe, Event, Faction, Location

# Create your views here.

def timeline_home(request):
    if request.user.is_authenticated:
        universe = Universe.objects.filter(owner=request.user).first()
    else:
        universe = Universe.objects.first() # seeded demo universe

    events = Event.objects.none()
    total_events = 0
    major_count = 0

    # For filter dropdown
    factions = Faction.objects.none()

    # Read query params
    selected_type = request.GET.get("type", "")
    selected_major = request.GET.get("major", "")
    selected_faction = request.GET.get("faction", "")

    if universe:
        factions = Faction.objects.filter(universe=universe).order_by("name")

        events = (
            Event.objects.filter(universe=universe)
            .select_related("location")
            .prefetch_related("factions")
        )

        # Apply filters
        if selected_type:
            events = events.filter(event_type=selected_type)

        if selected_major == "1":
            events = events.filter(is_major=True)

        if selected_faction:
            events = events.filter(factions__id=selected_faction)

        events = events.order_by("era", "year", "day", "created_at")

        total_events = events.count()
        major_count = events.filter(is_major=True).count()

    context = {
        "universe": universe,
        "events": events,
        "total_events": total_events,
        "major_count": major_count,
        "factions": factions,

        # keep selected values so dropdowns “stick”
        "selected_type": selected_type,
        "selected_major": selected_major,
        "selected_faction": selected_faction,

        # event type choices for dropdown
        "event_type_choices": Event.EventType.choices,
    }

    return render(request, "universe/timeline_home.html", context)


def event_detail(request, pk):
    event = get_object_or_404(
        Event.objects.select_related("universe", "location").prefetch_related("factions"),
        pk=pk,
        universe__owner=request.user,
    )

    context = {"event": event}
    return render(request, "universe/event_detail.html", context)


def factions_index(request):
    if request.user.is_authenticated:
        universe = Universe.objects.filter(owner=request.user).first()
    else:
        universe = Universe.objects.first() # seeded demo universe

    factions = Faction.objects.none()
    if universe:
        factions = (
            Faction.objects.filter(universe=universe)
            .annotate(event_count=Count("events", distinct=True))
            .order_by("name")
        )

    context = {
        "universe": universe,
        "factions": factions,
    }
    return render(request, "universe/factions_index.html", context)


def faction_detail(request, pk):
    faction = get_object_or_404(
        Faction.objects.select_related("universe"),
        pk=pk,
        universe__owner=request.user,
    )

    events = (
        Event.objects.filter(universe=faction.universe, factions=faction)
        .select_related("location")
        .prefetch_related("factions")
        .order_by("era", "year", "day", "created_at")
    )

    context = {
        "faction": faction,
        "events": events,
        "event_count": events.count(),
    }
    return render(request, "universe/faction_detail.html", context)


def locations_index(request):
    if request.user.is_authenticated:
        universe = Universe.objects.filter(owner=request.user).first()
    else:
        universe = Universe.objects.first() # seeded demo universe

    locations = Location.objects.none()
    if universe:
        locations = (
            Location.objects.filter(universe=universe)
            .select_related("controlling_faction")
            .annotate(event_count=Count("events", distinct=True))
            .order_by("name")  # alphabetical
        )

    context = {
        "universe": universe,
        "locations": locations,
    }
    return render(request, "universe/locations_index.html", context)



def location_detail(request, pk):
    location = get_object_or_404(
        Location.objects.select_related("universe", "controlling_faction"),
        pk=pk,
        universe__owner=request.user,
    )

    events = (
        Event.objects.filter(universe=location.universe, location=location)
        .select_related("location")
        .prefetch_related("factions")
        .order_by("era", "year", "day", "created_at")
    )

    context = {
        "location": location,
        "events": events,
        "event_count": events.count(),
    }
    return render(request, "universe/location_detail.html", context)


def search(request):
    if request.user.is_authenticated:
        universe = Universe.objects.filter(owner=request.user).first()
    else:
        universe = Universe.objects.first() # seeded demo universe

    q = (request.GET.get("q") or "").strip()

    events = Event.objects.none()
    factions = Faction.objects.none()
    locations = Location.objects.none()

    if universe and q:
        events = (
            Event.objects.filter(universe=universe)
            .filter(
                Q(title__icontains=q) |
                Q(summary__icontains=q)
            )
            .select_related("location")
            .prefetch_related("factions")
            .order_by("era", "year", "day", "created_at")
        )

        factions = (
            Faction.objects.filter(universe=universe)
            .filter(
                Q(name__icontains=q) |
                Q(short_name__icontains=q) |
                Q(description__icontains=q)
            )
            .order_by("name")
        )

        locations = (
            Location.objects.filter(universe=universe)
            .filter(
                Q(name__icontains=q) |
                Q(description__icontains=q)
            )
            .select_related("controlling_faction")
            .order_by("name")
        )

    context = {
        "universe": universe,
        "q": q,
        "events": events,
        "factions": factions,
        "locations": locations,
        "total_results": (events.count() + factions.count() + locations.count()) if (universe and q) else 0,
    }
    return render(request, "universe/search_results.html", context)