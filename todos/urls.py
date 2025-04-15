from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("action_add_new_todo", views.action_add_new_todo, name="action_add_new_todo"),
]
