from django.urls import path

from . import views


app_name = 'answers'
urlpatterns = [
    path('active_surveys/', views.ActiveSurveyView.as_view()),
]
