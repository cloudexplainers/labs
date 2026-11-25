from django.urls import path

from . import views

urlpatterns = [
    path("tasks/open/", views.open_tasks),
    path("jobs/<int:pk>/", views.job_detail),
]
