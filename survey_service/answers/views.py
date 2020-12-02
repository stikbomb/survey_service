""" Виды для работы с активными опросами - получение и заполнение. """
from rest_framework import status
from django.utils import timezone

from answers.models import PassedSurvey
from answers.serializers import (PassedSurveyCreateSerializer, PassedSurveyListSerializer,
                                 PassedSurveySimpleCreateSerializer)
from questionnaires.models import Questionnaire
from questionnaires.serializers import QuestionnaireSerializer
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.response import Response


class ActiveSurveyView(ListAPIView):
    """ Вид для получения всеъ активных опросов. """
    model = Questionnaire
    serializer_class = QuestionnaireSerializer

    def get_queryset(self):
        queryset = Questionnaire.objects.filter(
            beginning_date__lt=timezone.now(), expiration_date__gt=timezone.now())
        user_id = self.request.query_params.get('user', None)
        if user_id is not None:
            queryset = queryset.exclude(passed_surveys__user=user_id)

        return queryset


class PassedSurveyView(ListCreateAPIView):
    """ Вид для получения и сохранения пройденных опросов. """
    model = PassedSurvey
    serializer_class = PassedSurveyListSerializer
    post_serializer = PassedSurveyCreateSerializer

    def get_queryset(self):
        queryset = PassedSurvey.objects.all()
        user_id = self.request.query_params.get('user', None)
        if user_id is not None:
            queryset = queryset.filter(user=user_id)

        return queryset

    def post(self, request, *args, **kwargs):
        serializer = self.post_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        survey = serializer.save()
        headers = self.get_success_headers(serializer.data)
        result_serializer = self.get_serializer(survey)
        return Response(result_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PassedSurveySimpleCreateView(PassedSurveyView):
    """ Вид для сохранения опросов с упрощённым запросом и получения списка опросов. """
    post_serializer = PassedSurveySimpleCreateSerializer
