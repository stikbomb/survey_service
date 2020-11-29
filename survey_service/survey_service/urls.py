from django.urls import path, include


urlpatterns = [
    path('api/', include('questionnaires.urls')),
    path('api/', include('core.urls')),
    path('api/', include('answers.urls')),
]
