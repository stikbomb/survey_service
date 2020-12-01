""" Адреса URL для работы с опросами. """
from django.urls import path

from . import views


app_name = 'questionnaires'
urlpatterns = [
    path('questionnaires/', views.QuestionnaireLCView.as_view(), name='questionnaire_list'),
    path('questionnaire/<int:pk>/', views.QuestionnaireRUDView.as_view(), name='questionnaire_detail'),
    path('questions/', views.QuestionLCView.as_view(), name='question_list'),
    path('question/<int:pk>/', views.QuestionRUDView.as_view(), name='question_detail'),
    path('possible_answers/', views.PossibleAnswerCLView.as_view()),
    path('possible_answer/<int:pk>/', views.PossibleAnswerRUDView.as_view()),
]
