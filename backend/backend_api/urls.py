# backend/urls.py
from django.contrib import admin
from django.urls import path
from .views import get_setting, get_state_instance, send_message, send_file_by_url

urlpatterns = [
    # path("admin/", admin.site.urls),
    path("settings", get_setting, name='get_setting'),
    path("stateinstance", get_state_instance, name='get_state_instance'),
    path("sendmessage", send_message, name='send_message'),
    path("sendfilebyurl", send_file_by_url, name='send_file_by_url'),
]
