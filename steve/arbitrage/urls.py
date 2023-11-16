from django.urls import path

from .views import trigger

urlpatterns = [
    path("trigger", trigger),
]
