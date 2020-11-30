""" Виды для работы с активными опросами - получение и заполнение. """
from rest_framework import status
from django.utils import timezone

from answers.models import PassedSurvey
from answers.serializers import (PassedSurveyCreateSerializer, PassedSurveyListSerializer,
                                 PassesSurveySimpleCreateSerializer)
from questionnaires.models import Questionnaire
from questionnaires.serializers import QuestionnaireSerializer
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.response import Response


class ActiveSurveyView(ListAPIView):
    """ Вид для получения всеъ активных опросов. """

    def get_queryset(self):
        queryset = Questionnaire.objects.filter(
            beginning_date__lt=timezone.now(), expiration_date__gt=timezone.now())
        user_id = self.request.query_params.get('user', None)
        if user_id is not None:
            queryset = queryset.exclude(passed_surveys__user=user_id)

        return queryset

    model = Questionnaire
    serializer_class = QuestionnaireSerializer


# class ActiveSurveyByUserIdView(ActiveSurveyView):
#     """ Вид для получения активных опросов, которые не прошёл пользователь. """
#     def get(self, request, *args, **kwargs):
#         pk = kwargs['pk']
#         result = self.queryset.exclude(passed_surveys__user=pk)
#         serializer = self.get_serializer(result, many=True)
#         return Response(serializer.data)


class PassedSurveyByUserIdView(ListAPIView):
    """ Вид для получения опросов, которые прошёл пользователь. """
    queryset = PassedSurvey.objects.all()

    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        result = self.queryset.filter(user=pk)
        serializer = PassedSurveyListSerializer(result, many=True)
        return Response(serializer.data)


class PassedSurveyView(ListCreateAPIView):
    """ Вид для получения и сохранения пройденных опросов. """
    model = PassedSurvey

    def get_queryset(self):
        queryset = PassedSurvey.objects.all()
        user_id = self.request.query_params.get('user', None)
        if user_id is not None:
            queryset = queryset.filter(user=user_id)

        return queryset

    def get(self, request, *args, **kwargs):
        self.serializer_class = PassedSurveyListSerializer
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.serializer_class = PassedSurveyCreateSerializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        survey = serializer.save()
        headers = self.get_success_headers(serializer.data)
        result_serializer = PassedSurveyListSerializer(survey)
        return Response(result_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PassedSurveySimpleCreateView(PassedSurveyView):
    """ Вид для сохранения опросов с упрощённым запросом и получения списка опросов. """
    serializer_class = PassesSurveySimpleCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        survey = serializer.save()
        headers = self.get_success_headers(serializer.data)
        result_serializer = PassedSurveyListSerializer(survey)
        return Response(result_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
