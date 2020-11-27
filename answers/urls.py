from django.urls import path

from . import views


app_name = 'answers'
urlpatterns = [
    path('active_surveys/', views.ActiveSurveyView.as_view()),
    path('user/<int:pk>/active_surveys/', views.ActiveSurveyByUserIdView.as_view()),
]
