# backend/urls.py
from django.contrib import admin
from django.urls import path
from .views import get_setting, get_state_instance

urlpatterns = [
    # path("admin/", admin.site.urls),
    path("settings", get_setting, name='get_setting'),
    path("stateinstance", get_state_instance, name='get_state_instance'),
]
