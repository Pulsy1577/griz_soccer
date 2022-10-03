# pages/urls.py
from django.urls import path
from .views import HomePageView, dataView, indexView

urlpatterns = [
 path("", HomePageView.as_view(), name="home"),
 path("", dataView, name ="data"),
 path("templates/index.html", indexView.as_view(), name = "index"),
]