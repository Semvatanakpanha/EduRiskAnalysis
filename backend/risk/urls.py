from django.urls import path

from . import views

urlpatterns = [
    path("check-risk/", views.check_risk),
    path("history/", views.history),
]