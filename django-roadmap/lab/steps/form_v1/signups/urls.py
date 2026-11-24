from django.urls import path

from . import views

urlpatterns = [
    path("", views.dish_list),
    path("new/", views.sign_up),
]
