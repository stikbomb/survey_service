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
        self.client.post(self.url, questionnaire_data.correct_create_data(), format='json')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class PassedSurveysTest(APITestCase):
    def setUp(self):
        create_questionnaire(self)
        self.url = reverse('answers:passed_surveys')

    def test_create_passed_survey_correct_data(self):
        response = self.client.post(self.url, data.correct_data(), format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class AltPassedSurveysTest(APITestCase):
    def setUp(self):
        create_questionnaire(self)
        self.url = reverse('answers:alt_passed_surveys')

    def test_create_passed_survey_correct_data(self):
        response = self.client.post(self.url, data.correct_alt_data(), format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
