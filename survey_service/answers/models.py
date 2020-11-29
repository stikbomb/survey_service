"""
Модели для работы с пройдёнными опросами.
Поскольку активный опрос не защёщен от редактирования (кроме поля beginning_date) данные пройдённых запросов
будут сохраняться жётско, без привязки к моделям приложения questionnaire.
Единственное исключение - поле questionnaire в модели PassedSurvey, которое служит для фильтрации активных опросов
для конкретного пользователя по его числовому ID.
"""
from django.db.models import (Model, PositiveIntegerField, CharField, TextField, SET_NULL, DateField, ForeignKey,
                              DateTimeField, CASCADE)

from questionnaires.models import Questionnaire


class PassedSurvey(Model):
    """
    Модель пройдегго опроса.
    Включает в себя поля оригинального запроса, id пользователя, дату и время завершения опроса
    и ссылку на модель опроса. """
    user = PositiveIntegerField()
    created_at = DateTimeField()

    title = CharField(max_length=100)
    beginning_date = DateField()
    expiration_date = DateField()
    description = TextField()

    questionnaire = ForeignKey(
        Questionnaire,
        on_delete=SET_NULL,
        null=True,
        related_name='passed_surveys'
    )


class PassedQuestion(Model):
    """ Модель вопроса, на который получен ответ. """
    ANSWER_TYPES = (
        ('T', 'Text'),
        ('O', 'OneOf'),
        ('M', 'Many'),
    )

    text = TextField()
    type = CharField(max_length=1, choices=ANSWER_TYPES)

    survey = ForeignKey(
        PassedSurvey,
        on_delete=CASCADE,
        related_name='passed_questions'
    )


class Answer(Model):
    """ Модель ответа на пройденный вопрос. """
    text = CharField(max_length=250)

    passed_question = ForeignKey(
        PassedQuestion,
        on_delete=CASCADE,
        related_name='answers'
    )