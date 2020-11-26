""" Виды для работы с опросами, вопросами и вариантами ответов. """
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .serializers import QuestionnaireSerializer, QuestionSerializer, PossibleAnswerSerializer
from .models import Questionnaire, Question, PossibleAnswer


class QuestionnaireLCView(ListCreateAPIView):
    """ Вид для создания опроса и получения списка опросов. """
    queryset = Questionnaire.objects.all()
    model = Questionnaire
    serializer_class = QuestionnaireSerializer


class QuestionnaireRUDView(RetrieveUpdateDestroyAPIView):
    """ Вид для получение, реадктировани и удаления опроса по его ID. """
    model = Questionnaire
    serializer_class = QuestionnaireSerializer


class QuestionLCView(ListCreateAPIView):
    """ Вид для создания вопроса и получения списка всех вопросов. """
    queryset = Question.objects.all()
    model = Question
    serializer_class = QuestionSerializer


class QuestionRUDView(ListCreateAPIView):
    """ Вид для получения, редактирования и удаления вопроса по его ID. """
    model = Question
    serializer_class = QuestionSerializer


class PossibleAnswerCLView(ListCreateAPIView):
    """ Вид для создание ответа на вопрос и получение списка ответов. """
    queryset = PossibleAnswer.objects.all()
    model = PossibleAnswer
    serializer_class = PossibleAnswerSerializer


class PossibleAnswerRUDView(RetrieveUpdateDestroyAPIView):
    """ Вид для получения, редактирования и удаления вопроса по его ID. """
    model = PossibleAnswer
    serializer_class = PossibleAnswerSerializer