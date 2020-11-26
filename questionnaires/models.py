"""
Модели для работы с опросами.
"""
from django.db.models import Model, CharField, ForeignKey, CASCADE, TextField


class Questionnaire(Model):
    """
    Модель опроса.
    Опросник считается активным в промежутке дат между begining_date и expiration_date.
    После заполнения поля beginig_date нельзя добавлять, изменять или удалять вопросы в этом опросе.
    Удалить опрос можно в любом время.
    """
    pass


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
