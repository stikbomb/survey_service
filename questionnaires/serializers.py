""" Сериализаторы для работы с моделями опросов, вопросов и вариантов ответов. """
from rest_framework.serializers import ModelSerializer

from questionnaires.models import Questionnaire, Question, PossibleAnswer


class PossibleAnswerSerializer(ModelSerializer):
    """ Сериализатор возможного варианта ответа. """
    class Meta:
        model = PossibleAnswer
        fields = '__all__'


class QuestionSerializer(ModelSerializer):
    """ Сериализатор вопроса. """
    possible_answers = PossibleAnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = '__all__'


class QuestionnaireSerializer(ModelSerializer):
    """ Сериалазтор опроса. """
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Questionnaire
        fields = '__all__'
