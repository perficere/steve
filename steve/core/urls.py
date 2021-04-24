from django.urls import path

from .views import admin_site, health_check, trigger_error

urlpatterns = [
    path("admin", admin_site.urls),
    path("", health_check),
    path("error", trigger_error),
]
