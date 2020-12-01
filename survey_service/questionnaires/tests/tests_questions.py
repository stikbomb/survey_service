from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .data import questionnaire_data, question_data
from ..models import Questionnaire, Question


class QuestionsTest(APITestCase):
    def setUp(self):
        self.username = 'admin'
        self.email = 'admin@example.com'
        self.password = 123

        self.user = User.objects.create_superuser(self.username, self.email, self.password)
        self.client.login(username=self.username, password=self.password)
        self.client.post(reverse('questionnaires:questionnaire_list'),
                         questionnaire_data.correct_create_data(), format='json')
        self.questionnaire = Questionnaire.objects.all().first()

        self.url = reverse('questionnaires:question_list')

    def test_get_questions(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Question.objects.all().count())

    def test_create_question_correct_data(self):
        question_count_before_crete = Question.objects.all().count()
        self.client.post(self.url, question_data.correct_create_data(), format='json')
        self.assertEqual(Question.objects.all().count(), question_count_before_crete + 1)

    def test_create_question_incorrect_data_no_possible_answers(self):
        response = self.client.post(self.url, question_data.incorrect_create_data_no_possible_answers(), format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_question_incorrect_data_one_possible_answers(self):
        response = self.client.post(self.url, question_data.incorrect_create_data_one_possible_question(), format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_question_incorrect_data_possible_answers_wuth_text_type_question(self):
        data = question_data.incorrect_create_data_possible_answers_with_text_type_question()
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class QuestionTest(APITestCase):
    def setUp(self):
        self.username = 'admin'
        self.email = 'admin@example.com'
        self.password = 123

        self.user = User.objects.create_superuser(self.username, self.email, self.password)
        self.client.login(username=self.username, password=self.password)
        self.client.post(reverse('questionnaires:questionnaire_list'),
                         questionnaire_data.correct_create_data(), format='json')
        self.questionnaire = Questionnaire.objects.all().first()

    def get_url(self):
        return reverse('questionnaires:question_detail', kwargs={"pk": self.question_id})

    def test_get_question(self):
        question = Question.objects.filter(questionnaire=self.questionnaire.id).first()
        self.question_id = question.id
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.question_id)

    def test_success_question_delete(self):
        question = Question.objects.filter(questionnaire=self.questionnaire.id).last()
        question_count_before_delete = Question.objects.filter(questionnaire=self.questionnaire.id).count()
        self.question_id = question.id
        response = self.client.delete(self.get_url())
        question_count_after_delete = Question.objects.filter(questionnaire=self.questionnaire.id).count()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(question_count_after_delete, question_count_before_delete - 1)

    def test_failed_question_delete_one_question_left(self):
        question = Question.objects.filter(questionnaire=self.questionnaire.id).last()
        self.question_id = question.id
        self.client.delete(self.get_url())

        question_count_before_delete = Question.objects.filter(questionnaire=self.questionnaire.id).count()
        question = Question.objects.filter(questionnaire=self.questionnaire.id).last()
        self.question_id = question.id
        response = self.client.delete(self.get_url())
        question_count_after_delete = Question.objects.filter(questionnaire=self.questionnaire.id).count()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(question_count_after_delete, question_count_before_delete)

    def test_put_correct_data(self):
        question = Question.objects.filter(questionnaire=self.questionnaire.id).first()
        self.question_id = question.id
        data = question_data.correct_put_data()
        response = self.client.put(self.get_url(), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['text'], data['text'])

    def test_put_incorrect_data_type_field_change(self):
        question = Question.objects.filter(questionnaire=self.questionnaire.id).first()
        self.question_id = question.id
        data = question_data.incorrect_put_data_type_field_change()
        response = self.client.put(self.get_url(), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
