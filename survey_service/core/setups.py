from django.contrib.auth.models import User
from django.urls import reverse

from questionnaires.tests.data import questionnaire_data


def admin_login(self):
    self.username = 'admin'
    self.email = 'admin@example.com'
    self.password = 123

    self.user = User.objects.create_superuser(self.username, self.email, self.password)
    self.client.login(username=self.username, password=self.password)

def create_questionnaire(self, login=False):
    self.username = 'admin'
    self.email = 'admin@example.com'
    self.password = 123

    self.user = User.objects.create_superuser(self.username, self.email, self.password)
    self.client.login(username=self.username, password=self.password)
    self.client.post(reverse('questionnaires:questionnaire_list'),
                     questionnaire_data.correct_create_data(), format='json')
    if not login:
        self.client.logout()