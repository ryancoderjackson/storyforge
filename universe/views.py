from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Universe, Event

# Create your views here.
@login_required
def timeline_home(request):
    # Temporary approach: pick the first universe for this user
    universe = Universe.objects.filter(owner=request.user).first()

    # If no universe exists yet, show an empty state
    events = Event.objects.none()
    if universe:
        events = (
            Event.objects.filter(universe=universe)
            .select_related("location")
            .prefetch_related("factions")
            .order_by("era", "year", "day", "created_at")
        )

    total_events = events.count()
    major_count = events.filter(is_major=True).count()

    context = {
        "universe": universe,
        "events": events,
        "total_events": total_events,
        "major_count": major_count,
    }
    return render(request, "universe/timeline_home.html", context)

@login_required
def event_detail(request, pk):
    event = get_object_or_404(
        Event.objects.select_related("universe", "location").prefetch_related("factions"),
        pk=pk,
        universe__owner=request.user,
    )

    context = {"event": event}
    return render(request, "universe/event_detail.html", context)