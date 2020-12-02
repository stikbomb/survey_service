from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from . import data
from questionnaires.tests.data import questionnaire_data
from core.setups import create_questionnaire


class ActiveSurveysTest(APITestCase):
    def setUp(self):
        create_questionnaire(self)
        self.url = reverse('answers:active_surveys')

    def test_get_active_surveys(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_active_surveys_by_user(self):
        response = self.client.get(self.url, {'user': data.correct_data()['user']})
        self.assertEqual(len(response.data), 1)
        self.client.post(reverse('answers:passed_surveys'), data.correct_data(), format='json')
        response = self.client.get(self.url, {'user': data.correct_data()['user']})
        self.assertEqual(len(response.data), 0)


class PassedSurveysTest(APITestCase):
    def setUp(self):
        create_questionnaire(self)
        self.url = reverse('answers:passed_surveys')

    def test_create_passed_survey_correct_data(self):
        response = self.client.post(self.url, data.correct_data(), format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_passed_survey_by_user(self):
        self.client.post(self.url, data.correct_data(), format='json')
        self.client.post(self.url, data.correct_data_another_user(), format='json')
        response = self.client.get(self.url, {'user': data.correct_data()['user']})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user'], data.correct_data()['user'])
        self.assertNotEqual(response.data[0]['user'], data.correct_data_another_user()['user'])


class AltPassedSurveysTest(APITestCase):
    def setUp(self):
        create_questionnaire(self)
        self.url = reverse('answers:alt_passed_surveys')

    def test_create_passed_survey_correct_data(self):
        response = self.client.post(self.url, data.correct_alt_data(), format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
