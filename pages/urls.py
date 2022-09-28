# pages/urls.py
from django.urls import path
from .views import HomePageView, dataView

urlpatterns = [
 path("", HomePageView.as_view(), name="home"),
 path("", dataView, name ="data"),
]