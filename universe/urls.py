from django.urls import path
from .views import timeline_home

app_name = "universe"

urlpatterns = [
    path("", timeline_home, name="timeline_home"),
]