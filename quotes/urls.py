from django.urls import path

from . import views

app_name = "quotes"

urlpatterns = [
    path("", views.random_quote, name="random"),
    path("losuj/", views.reroll, name="reroll"),
    path("dodaj/", views.add_quote, name="add"),
]
