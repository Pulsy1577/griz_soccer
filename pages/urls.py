# pages/urls.py
from django.urls import path, include, re_path
from .views import DashboardView, aboutView, dataView HomePageView, indexView, session_state_view

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    # path("", dataView, name="data"),
    path("templates/index.html", indexView.as_view(), name="index"),
    # path("templates/dash_test.html", DashboardView.as_view(), name="dash_test"),

    re_path(
        "dash_test",
        session_state_view,
        {"template_name": "dash_test.html"},
        name="dash_test",
    ),

    #paths for other pages
    path("templates/about.html", aboutView.as_view() name='about'),
    path("templates/data.html"), dataView.as_view(), name='data'),
]
