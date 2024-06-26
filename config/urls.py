from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include


urlpatterns = i18n_patterns(
    path("admin/", admin.site.urls),
    path("api/", include("api.router")),
)
