from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.response import Response
from django.utils import timezone

from questionnaires.models import Questionnaire
from questionnaires.serializers import QuestionnaireSerializer


class ActiveSurveyView(ListAPIView):
    queryset = Questionnaire.objects.filter(
        beginning_date__lt=timezone.now(), expiration_date__gt=timezone.now())
    model = Questionnaire
    serializer_class = QuestionnaireSerializer


class ActiveSurveyByUserIdView(ActiveSurveyView):
    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        result = self.queryset.exclude(passed_surveys__user=pk)
        serializer = self.get_serializer(result, many=True)
        return Response(serializer.data)

