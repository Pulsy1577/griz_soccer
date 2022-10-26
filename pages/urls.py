# pages/urls.py
from django.urls import path, include
from .views import DashboardView, HomePageView, indexView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    #path("", dataView, name="data"),
    path("templates/index.html", indexView.as_view(), name="index"),
    path("templates/dash_test.html", DashboardView.as_view(), name="dash_test"),
]
