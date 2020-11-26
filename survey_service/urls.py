
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('api/', include('questionnaires.urls')),
    path('api/', include('core.urls')),
]