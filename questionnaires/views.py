""" Виды для работы с опросами, вопросами и вариантами ответов. """
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser

from .serializers import QuestionnaireSerializer, QuestionSerializer, PossibleAnswerSerializer
from .models import Questionnaire, Question, PossibleAnswer
from core.exceptions import DeletionError, EditionError


class QuestionnaireLCView(ListCreateAPIView):
    """ Вид для создания опроса и получения списка опросов. """
    permission_classes = (IsAdminUser,)

    queryset = Questionnaire.objects.all()
    model = Questionnaire
    serializer_class = QuestionnaireSerializer


class QuestionnaireRUDView(RetrieveUpdateDestroyAPIView):
    """ Вид для получение, редактирования и удаления опроса по его ID. """
    permission_classes = (IsAdminUser,)

    queryset = Questionnaire.objects.all()
    model = Questionnaire
    serializer_class = QuestionnaireSerializer

    def _check_beginning_date_change(self, request):
        print(request.data['beginning_date'])
        print(self.get_object().beginning_date)
        try:
            if request.data['beginning_date'] != str(self.get_object().beginning_date):
                raise EditionError('Поле "beginning_date" нельзя отредактировать.')
        except KeyError:
            pass

    def patch(self, request, *args, **kwargs):
        self._check_beginning_date_change(request)
        return super().patch(self, request, *args, **kwargs)


class QuestionLCView(ListCreateAPIView):
    """ Вид для создания вопроса и получения списка всех вопросов. """
    permission_classes = (IsAdminUser,)

    queryset = Question.objects.all()
    model = Question
    serializer_class = QuestionSerializer


class QuestionRUDView(RetrieveUpdateDestroyAPIView):
    """ Вид для получения, редактирования и удаления вопроса по его ID. """
    permission_classes = (IsAdminUser,)

    queryset = Question.objects.all()
    model = Question
    serializer_class = QuestionSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if Question.objects.filter(questionnaire_id=instance.questionnaire).count() == 2:
            raise DeletionError(detail='Невозможно удалить вопрос: опрос должен содержать минимум два вопроса.')

        return super().delete(self, request, *args, **kwargs)


class PossibleAnswerCLView(ListCreateAPIView):
    """ Вид для создание ответа на вопрос и получение списка ответов. """
    permission_classes = (IsAdminUser,)

    queryset = PossibleAnswer.objects.all()
    model = PossibleAnswer
    serializer_class = PossibleAnswerSerializer


class PossibleAnswerRUDView(RetrieveUpdateDestroyAPIView):
    """ Вид для получения, редактирования и удаления вопроса по его ID. """
    permission_classes = (IsAdminUser,)

    queryset = PossibleAnswer.objects.all()
    model = PossibleAnswer
    serializer_class = PossibleAnswerSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if PossibleAnswer.objects.filter(question_id=instance.questions).count() == 2:
            raise DeletionError(
                detail='Невозможно удалить вариант отвека: вопрос должен содержать минимум два варианта.')

        return super().delete(self, request, *args, **kwargs)
