from django.urls import path

from . import views


app_name = 'questionnaires'
urlpatterns = [
    path('questionnaires/', views.QuestionnaireLCView.as_view()),
    path('questionnaire/<int:pk>/', views.QuestionnaireRUDView.as_view()),
    path('questions/', views.QuestionLCView.as_view()),
    path('question/<int:pk>', views.QuestionRUDView.as_view()),
    path('possible_answers/', views.PossibleAnswerCLView.as_view()),
    path('possible_answer/<int:pk>', views.PossibleAnswerRUDView.as_view()),
]
