from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from universe.models import Universe, Faction, Location, Event


class Command(BaseCommand):
    help = "Seed demo data for StoryForge (Cosmic Impact universe). Safe to run multiple times."

    def add_arguments(self, parser):
        parser.add_argument(
            "--username",
            type=str,
            default=None,
            help="Username that will own the seeded Universe. Defaults to first superuser, then first user.",
        )

    def handle(self, *args, **options):
        User = get_user_model()
        username = options.get("username")

        owner = None
        if username:
            owner = User.objects.filter(username=username).first()
            if not owner:
                self.stdout.write(self.style.ERROR(f'User "{username}" not found.'))
                return
        else:
            owner = User.objects.filter(is_superuser=True).first() or User.objects.first()

        if not owner:
            owner, created = User.objects.get_or_create(
                username="demo",
                defaults={
                    "email": "demo@example.com",
                    "is_staff": True,
                    "is_superuser": True,
                },
            )
            if created:
                owner.set_password("demo12345")  # or something you choose
                owner.save()
            return

        # --- Universe ---
        universe, universe_created = Universe.objects.get_or_create(
            owner=owner,
            name="Cosmic Impact",
            defaults={
                "is_demo": True,
                "tagline": "A universe reshaped by The Rapture.",
                "description": (
                    "Cosmic Impact is a dark sci-fi universe centered on a catastrophic event known as "
                    "The Rapture — the sudden disappearance of half of humanity — followed by peaceful "
                    "but suspicious first contact with the Idol'Rehn-Vaar."
                ),
            },
        )

        # If it already existed, ensure flag is set
        if not universe.is_demo:
            universe.is_demo = True
            universe.save(update_fields=["is_demo"])

        # --- Factions ---
        hca, _ = Faction.objects.get_or_create(
            universe=universe,
            name="Human Coalition Authority",
            defaults={
                "short_name": "HCA",
                "alignment": Faction.Alignment.NEUTRAL,
                "description": (
                    "A provisional global governing body formed in the aftermath of The Rapture to coordinate "
                    "humanitarian response, military stability, and diplomatic engagement."
                ),
            },
        )

        idols, _ = Faction.objects.get_or_create(
            universe=universe,
            name="Idol'Rehn-Vaar",
            defaults={
                "short_name": "Idols",
                "alignment": Faction.Alignment.ORDER,
                "description": (
                    "An advanced extraterrestrial civilization that views itself as custodians of cosmic order. "
                    "They believe chaotic species must be guided toward stability before integration into the "
                    "broader galactic community."
                ),
            },
        )

        # --- Locations ---
        earth, _ = Location.objects.get_or_create(
            universe=universe,
            name="Earth",
            defaults={
                "location_type": Location.LocationType.PLANET,
                "description": (
                    "Humanity's homeworld and the epicenter of The Rapture. In its wake, Earth enters a period "
                    "of political instability and cultural fracture."
                ),
                "controlling_faction": hca,
            },
        )

        # Ensure controlling faction stays set if Earth existed already
        if earth.controlling_faction_id is None:
            earth.controlling_faction = hca
            earth.save(update_fields=["controlling_faction"])

        earth_orbit, _ = Location.objects.get_or_create(
            universe=universe,
            name="Earth Orbit",
            defaults={
                "location_type": Location.LocationType.ORBIT,
                "description": (
                    "The region of space surrounding Earth where the Idol'Rehn-Vaar vessel first manifested "
                    "and initiated global communication."
                ),
                "controlling_faction": None,
            },
        )

        # --- Events ---
        rapture, _ = Event.objects.get_or_create(
            universe=universe,
            era=Event.Era.PI,
            year=0,
            day=0,
            defaults={
                "title": "The Rapture",
                "summary": "...",
                "event_type": Event.EventType.CATASTROPHE,
                "location": earth,
                "is_major": True,
            },
        )
        if rapture.factions.count() == 0:  # only set if no factions yet to avoid duplicates on multiple runs
            rapture.factions.set([hca])

        first_contact, _ = Event.objects.get_or_create(
            universe=universe,
            era=Event.Era.PI,
            year=0,
            day=7,
            defaults={
                "title": "Orbital Emergence / First Contact",
                "summary": "...",
                "event_type": Event.EventType.DIPLOMACY,
                "location": earth_orbit,
                "is_major": True,
            },
        )
        if first_contact.factions.count() == 0:  # same logic as above to avoid duplicates
            first_contact.factions.set([hca, idols])

        # --- Output ---
        self.stdout.write(self.style.SUCCESS("✅ StoryForge demo data seeded."))
        self.stdout.write(f"Owner: {owner.username}")
        self.stdout.write(f"Universe: {universe.name}")
        self.stdout.write("Created/verified: factions, locations, events")