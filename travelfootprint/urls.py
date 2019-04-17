from django.http.response import HttpResponse
from django.urls import path

from . import views

urlpatterns = [
    path("_ah/health", lambda _: HttpResponse("OK"), name="healthcheck"),
    path("", views.IndexView.as_view(), name="index"),
    path("<username>/", views.ProfileView.as_view(), name="profile"),
]
