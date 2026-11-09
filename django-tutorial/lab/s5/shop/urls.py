from django.urls import path

from . import views

urlpatterns = [
    path("", views.tea_list, name="tea_list"),
    path("teas/<slug:slug>/", views.tea_detail, name="tea_detail"),
    path("teas/<slug:slug>/order/", views.order, name="order"),
    path("thanks/", views.thanks, name="thanks"),
]
