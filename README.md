# StoryForge

StoryForge is a Django-based sci-fi universe management system designed to model fictional worlds as structured relational data. 

It organizes universes into factions, locations, and chronological events, then presents them through a searchable and filterable “cosmic archive” interface.

This capstone project uses **Django Admin as the authoring tool** and a custom front-end for browsing, filtering, and exploring the universe.

🔗 Live Demo: https://storyforge-9m85.onrender.com
The deployed demo includes a pre-seeded universe ("Cosmic Impact") for immediate exploration.

---

## Features
- Timeline home view with sortable chronological event feed
- Filters by event type, faction, and “major events”
- Universe-wide search across events, factions, and locations
- Event detail pages with linked factions and locations
- Factions index + faction detail pages with related timeline events
- Locations index + location detail pages with related timeline events
- `seed_demo` command for one-step demo data setup (Cosmic Impact universe)
- Production deployment with migrations + static handling

---

## Demo Data
StoryForge includes a seed_demo management command that populates a demo universe called Cosmic Impact, including factions, locations, and major timeline events.

---

## Screenshots

### Events
![Events](screenshots/event-timeline.png)

### Event Detail
![Event Detail](screenshots/event-detail.png)

### Search
![Search Results](screenshots/search-results.png)

### Factions
![Factions](screenshots/factions-index.png)

### Faction Detail
![Faction Detail](screenshots/faction-detail.png)

### Locations
![Locations](screenshots/locations-index.png)

### Location Detail
![Location Detail](screenshots/location-detail.png)

---

## Why This Project

StoryForge was built as a capstone backend project to demonstrate:
- Relational data modeling
- Query optimization
- Production deployment workflow
- Scalable content architecture for creative systems

---

## Tech Stack
- Python
- Django
- SQLite (dev)
- HTML/CSS (custom theme) + Bootstrap (light usage)
- PostgreSQL (Render)
- Gunicorn
- WhiteNoise (static files)

---

## Architecture Highlights

- Abstract base model for timestamp tracking
- Use of Django model relationships (ForeignKey, ManyToMany)
- Query optimization with select_related and prefetch_related
- Custom management command (seed_demo) for demo data
- Environment-based production configuration
- Automated migrations during deployment
- Clear separation between content authoring (Django Admin) and public presentation layer

---

## Quickstart (Local Setup)
```bash
git clone https://github.com/ryancoderjackson/storyforge.git
cd storyforge
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
# Create a superuser if you’d like to access the Django Admin panel:
python manage.py createsuperuser