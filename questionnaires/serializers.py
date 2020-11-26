""" Сериализаторы для работы с моделями опросов, вопросов и вариантов ответов. """
from rest_framework.serializers import ModelSerializer, ValidationError, RelatedField, PrimaryKeyRelatedField

from questionnaires.models import Questionnaire, Question, PossibleAnswer


class PossibleAnswerSerializer(ModelSerializer):
    """ Сериализатор возможного варианта ответа. """

    class Meta:
        model = PossibleAnswer
        exclude = ('question',)


class QuestionSerializer(ModelSerializer):
    """ Сериализатор вопроса. """
    possible_answers = PossibleAnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = '__all__'

    def validate(self, attrs):
        if attrs['type'] in ('O', 'M') and len(attrs['possible_answers']) < 2:
            raise ValidationError('Вопрос с вариантами ответа должен иметь минимум два возможных ответа.')

        if attrs['type'] == 'T' and attrs['possible_answers']:
            raise ValidationError('Вопрос с текстовым ответом не должен иметь вариантов ответа.')

        return attrs

    def create(self, validated_data, **kwargs):
        possible_answers_data = validated_data.pop('possible_answers')
        question = Question.objects.create(**validated_data)
        for answer_data in possible_answers_data:
            PossibleAnswer.objects.create(question=question, **answer_data)

        return question


class QuestionnaireSerializer(ModelSerializer):
    """ Сериалазтор опроса. """
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Questionnaire
        fields = '__all__'
