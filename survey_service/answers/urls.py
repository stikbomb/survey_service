""" Пути URL для работы с активными опросами - получени и заполнение. """
from django.urls import path

from . import views


app_name = 'answers'
urlpatterns = [
    path('active_surveys/', views.ActiveSurveyView.as_view()),
    path('passed_surveys/', views.PassedSurveyView.as_view()),
    path('alternative_passed_surveys/', views.PassedSurveySimpleCreateView.as_view())
]
