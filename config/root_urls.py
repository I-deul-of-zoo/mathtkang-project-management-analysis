from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

urlpatterns = [
    # [end-point]
    path('admin/', admin.site.urls),
    path('api/auths/', include('auths.urls')),
    path('api/kanbans/', include('kanbans.urls')),
    path('api/teams/', include('teams.urls')),
]