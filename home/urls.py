from django.urls import path

from .views import HomePageView, simulationView

urlpatterns = [
    path("", HomePageView, name="homepage"),
    path("simulation.result/", simulationView, name="result"),
]