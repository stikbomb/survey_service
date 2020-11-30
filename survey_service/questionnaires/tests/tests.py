from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .data import questionnaire_data
from ..models import Questionnaire


class QuestionnairesTests(APITestCase):
    def setUp(self):
        self.username = 'admin'
        self.email = 'admin@example.com'
        self.password = 123

        self.user = User.objects.create_superuser(self.username, self.email, self.password)
        self.client.login(username=self.username, password=self.password)

        self.url = reverse('questionnaires:questionnaire_list')

    def test_create_questionnaire_correct_create_data(self):
        response = self.client.post(self.url, questionnaire_data.correct_create_data(), format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Questionnaire.objects.all().count(), 1)

    def test_get_questionnaires(self):
        self.client.post(self.url, questionnaire_data.correct_create_data(), format='json')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_questionnaire_incorrect_create_data_one_question(self):
        response = self.client.post(self.url,
                                    questionnaire_data.incorrect_create_data_one_question(), format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_questionnaire_incorrect_create_data_one_possible_answer(self):
        response = self.client.post(self.url,
                                    questionnaire_data.incorrect_create_data_one_possible_answer(), format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_questionnaire_incorrect_create_data_wrong_field_name(self):
        response = self.client.post(self.url,
                                    questionnaire_data.incorrect_create_data_wrong_field_name(), format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class QuestionnaireTest(APITestCase):
    def setUp(self):
        self.username = 'admin'
        self.email = 'admin@example.com'
        self.password = 123

        self.user = User.objects.create_superuser(self.username, self.email, self.password)
        self.client.login(username=self.username, password=self.password)
        self.client.post(reverse('questionnaires:questionnaire_list'),
                         questionnaire_data.correct_create_data(), format='json')
        self.questionnaire = Questionnaire.objects.all().first()

        self.url = reverse('questionnaires:questionnaire_detail', kwargs={"pk": self.questionnaire.pk})

    def test_get_questionnaire(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.questionnaire.pk)
    
    def test_update_questionnaire_correct_data(self):
        data = questionnaire_data.correct_put_data()
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], data['title'])

    def test_update_questionnaire_incorrect_put_data_change_beginning_date(self):
        data = questionnaire_data.incorrect_put_data_change_beginning_date()
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_questionnaire_incorrect_put_data_nested_objects(self):
        data = questionnaire_data.incorrect_put_data_nested_objects()
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_questionnaire_incorrect_put_data_wrong_expiration_date(self):
        data = questionnaire_data.incorrect_put_data_wrong_expiration_date()
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_questionnaire(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)