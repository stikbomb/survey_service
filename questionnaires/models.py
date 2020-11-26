"""
Модели для работы с опросами.
"""
from django.db.models import Model, CharField, ForeignKey, CASCADE, TextField, DateField


class Questionnaire(Model):
    """
    Модель опроса.
    Опросник считается активным в промежутке дат между beginning_date и expiration_date.
    После заполнения поля beginning_date нельзя добавлять, изменять или удалять вопросы в этом опросе.
    Удалить опрос можно в любом время.
    """
    title = CharField(max_length=100)
    beginning_date = DateField(null=True, blank=True)
    expiration_date = DateField(null=True, blank=True)
    description = TextField(blank=True, default='')


class Question(Model):
    """
    Вопросы, из которых состоит опрос.
    Могут быть трёх типов:
        - ответ текстом (T);
        - ответ с выбором одного варианта (O);
        - ответ с выбором нескольких вариантов (M).
    В двух последних типах допустимо наличие только одного варианта ответа.
    Все поля обязательны для заполнения.
    При удалении опроса удаляются все связанные с ним вопросы.
    """
    ANSWER_TYPES = (
        ('T', 'Text'),
        ('O', 'OneOf'),
        ('M', 'Many'),
    )

    text = TextField()
    type = CharField(max_length=1, choices=ANSWER_TYPES)
    questionnaire = ForeignKey(
        Questionnaire,
        on_delete=CASCADE,
        related_name='questions'
    )


class PossibleAnswer(Model):
    """
    Возможные варианты ответов для вопросов, в которых это предусмотрено.
    Все поля обязательны для заполнения.
    При удалении вопроса удаляются все связанные с ним варианты ответов.
    """
    text = CharField(max_length=250)

    question = ForeignKey(
        Question,
        on_delete=CASCADE,
        related_name='possible_answers'
    )
