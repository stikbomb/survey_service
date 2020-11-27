from rest_framework.generics import ListAPIView, ListCreateAPIView
from django.utils import timezone

from questionnaires.models import Questionnaire
from questionnaires.serializers import QuestionnaireSerializer


class ActiveSurveyView(ListAPIView):
    queryset = Questionnaire.objects.filter(
        beginning_date__lt=timezone.now(), expiration_date__gt=timezone.now())
    model = Questionnaire
    serializer_class = QuestionnaireSerializer
