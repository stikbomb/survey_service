""" Виды для работы с опросами, вопросами и вариантами ответов. """
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser

from .serializers import QuestionnaireSerializer, QuestionSerializer, PossibleAnswerSerializer
from .models import Questionnaire, Question, PossibleAnswer


class QuestionnaireLCView(ListCreateAPIView):
    """ Вид для создания опроса и получения списка опросов. """
    permission_classes = (IsAdminUser,)

    queryset = Questionnaire.objects.all()
    model = Questionnaire
    serializer_class = QuestionnaireSerializer


class QuestionnaireRUDView(RetrieveUpdateDestroyAPIView):
    """ Вид для получение, редактирования и удаления опроса по его ID. """
    permission_classes = (IsAdminUser,)

    model = Questionnaire
    serializer_class = QuestionnaireSerializer


class QuestionLCView(ListCreateAPIView):
    """ Вид для создания вопроса и получения списка всех вопросов. """
    permission_classes = (IsAdminUser,)

    queryset = Question.objects.all()
    model = Question
    serializer_class = QuestionSerializer


class QuestionRUDView(RetrieveUpdateDestroyAPIView):
    """ Вид для получения, редактирования и удаления вопроса по его ID. """
    permission_classes = (IsAdminUser,)

    model = Question
    serializer_class = QuestionSerializer


class PossibleAnswerCLView(ListCreateAPIView):
    """ Вид для создание ответа на вопрос и получение списка ответов. """
    permission_classes = (IsAdminUser,)

    queryset = PossibleAnswer.objects.all()
    model = PossibleAnswer
    serializer_class = PossibleAnswerSerializer


class PossibleAnswerRUDView(RetrieveUpdateDestroyAPIView):
    """ Вид для получения, редактирования и удаления вопроса по его ID. """
    permission_classes = (IsAdminUser,)

    model = PossibleAnswer
    serializer_class = PossibleAnswerSerializer
