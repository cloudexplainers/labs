from django.contrib import admin
from django.urls import path

from menu import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("teas/", views.list_teas),
    path("supplier/", views.supplier),
    path("supplier-async/", views.supplier_async),
]
