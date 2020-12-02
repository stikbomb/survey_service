""" Пути URL для работы с активными опросами - получени и заполнение. """
from django.urls import path

from . import views


app_name = 'answers'
urlpatterns = [
    path('active_surveys/', views.ActiveSurveyView.as_view(), name='active_surveys'),
    path('passed_surveys/', views.PassedSurveyView.as_view(), name='passed_surveys'),
    path('alternative_passed_surveys/', views.PassedSurveySimpleCreateView.as_view(), name='alt_passed_surveys')
]
