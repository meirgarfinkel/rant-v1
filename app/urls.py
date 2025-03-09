from django.contrib import admin
from django.urls import path, include
from app import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls", namespace="users")),
    path("suggestions/", include("suggestions.urls", namespace="suggestions")),
    path("", views.HomeView.as_view(), name="home"),
]
