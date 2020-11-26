""" Сериализаторы для работы с моделями опросов, вопросов и вариантов ответов. """
from rest_framework.serializers import ModelSerializer

from questionnaires.models import Questionnaire, Question, PossibleAnswer


class PossibleAnswerSerializer(ModelSerializer):

    class Meta:
        model = PossibleAnswer
        fields = '__all__'


class QuestionSerializer(ModelSerializer):
    possible_answers = PossibleAnswerSerializer(read_only=True, many=True)

    class Meta:
        model = Question
        fields = '__all__'


class QuestionnaireSerializer(ModelSerializer):
    questions = QuestionSerializer(read_only=True, many=True)

    class Meta:
        model = Questionnaire
        fields = '__all__'
