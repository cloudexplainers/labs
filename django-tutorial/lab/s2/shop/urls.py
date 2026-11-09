from django.urls import path

from . import views

urlpatterns = [
    path("", views.tea_list, name="tea_list"),
]
