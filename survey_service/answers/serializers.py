""" Сериализаторы для работы с активными опросами. """
from rest_framework.serializers import (Serializer, PrimaryKeyRelatedField, ChoiceField, ListSerializer, CharField,
                                        IntegerField, SlugRelatedField, ModelSerializer)
from django.utils import timezone
from django.forms.models import model_to_dict
from django.db import transaction

from questionnaires.models import Questionnaire, Question, PossibleAnswer
from .models import PassedSurvey, PassedQuestion, Answer


class PassedQuestionSerializer(Serializer):
    """ Сериализатор для создания вопросов и ответов с пройденном опросе. """
    question = IntegerField(write_only=True)
    type = ChoiceField(['T', 'O', 'M'])
    answers = ListSerializer(child=CharField())
    survey = PrimaryKeyRelatedField(queryset=PassedSurvey.objects.all(), required=False)

    def _normalize_answers(self, answers, question_type):
        """ Приводит ответы к единой форме в зависимости от типа вопроса. """
        result = []
        if question_type != 'T':
            for answer in answers:
                possible_answer = PossibleAnswer.objects.get(id=answer)
                result.append({'text': possible_answer.text})
        else:
            result = [{'text': answers[0]}]

        return result

    def create(self, validated_data):
        answers_data = validated_data.pop('answers')
        question_id = validated_data.pop('question')
        question = Question.objects.get(id=question_id)
        validated_data.update({'text': question.text})
        passed_question = PassedQuestion.objects.create(**validated_data)

        answers_data = self._normalize_answers(answers_data, validated_data['type'])

        for answer_data in answers_data:
            Answer.objects.create(passed_question=passed_question, **answer_data)
        return passed_question


class PassedSurveyCreateSerializer(Serializer):
    """ Сериализатор для создания пройденного опроса. """
    questionnaire = PrimaryKeyRelatedField(queryset=Questionnaire.objects.all())
    user = IntegerField()
    passed_questions = PassedQuestionSerializer(many=True)

    @transaction.atomic
    def create(self, validated_data):
        questions_data = validated_data.pop('passed_questions')
        survey_data = model_to_dict(validated_data['questionnaire'])
        survey_data.pop('id')
        survey_data.update({
            'user': validated_data['user'],
            'created_at': timezone.now(),
            'questionnaire': validated_data['questionnaire']
        })
        passed_survey = PassedSurvey.objects.create(**survey_data)

        for question_data in questions_data:
            question_data['survey'] = passed_survey.id
            question_serializer = PassedQuestionSerializer(data=question_data)
            if question_serializer.is_valid(raise_exception=True):
                question_serializer.save()

        return passed_survey


class PassedQuestionListSerializer(ModelSerializer):
    """ Сериализатор для вывода списка пройденных вопросов и ответов. """
    answers = SlugRelatedField(many=True, read_only=True, slug_field='text')

    class Meta:
        model = PassedQuestion
        fields = ('text', 'type', 'answers')


class PassedSurveyListSerializer(ModelSerializer):
    """ Сериализатор для вывода списка пройденных опросов. """
    passed_questions = PassedQuestionListSerializer(many=True)

    class Meta:
        model = PassedSurvey
        fields = ('user', 'title', 'beginning_date', 'expiration_date', 'description', 'passed_questions')


class AnswerSerializer(ModelSerializer):
    """ Сериализатор для ответа пройденного опроса с простой формой запроса. """
    class Meta:
        model = Answer
        fields = ('text',)


class PassedQuestionSimpleCreateSerializer(ModelSerializer):
    """ Сериализатор для добавления вопроса пройденного опроса с простой формой запроса. """
    answers = AnswerSerializer(many=True)
    survey = PrimaryKeyRelatedField(queryset=PassedSurvey.objects.all(), write_only=True, required=False)

    class Meta:
        model = PassedQuestion
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        answers_data = validated_data.pop('answers')

        question = PassedQuestion.objects.create(**validated_data)

        for answer_data in answers_data:
            Answer.objects.create(passed_question=question, **answer_data)

        return question


class PassedSurveySimpleCreateSerializer(ModelSerializer):
    """ Сериализатор для добавления пройденного опроса с простой формой запроса. """
    passed_questions = PassedQuestionSimpleCreateSerializer(many=True)

    class Meta:
        model = PassedSurvey
        fields = '__all__'

    def create(self, validated_data):
        questions_data = validated_data.pop('passed_questions')
        survey = PassedSurvey.objects.create(**validated_data)

        for question_data in questions_data:
            question_data.update({'survey': survey.id})

        questions_serializer = PassedQuestionSimpleCreateSerializer(data=questions_data, many=True)
        if questions_serializer.is_valid(raise_exception=True):
            questions_serializer.save()

        return survey
