from django.urls import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import User


class UserTests(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='admin',
                                             email='admin@admin.com',
                                             password='admin')

    def test_create_account(self):
        url = reverse('accounts:signup')

        data = {'username': 'yektanet', 'email': 'yek@ta.net',
                'password': '123456', 'repeat_password': '123456'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.get(email='yek@ta.net').username,
                         'yektanet')

    def test_login_username(self):
        url = reverse('accounts:login')
        data = {'username': 'admin', 'password': 'admin'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'token')

    def test_login_email(self):
        url = reverse('accounts:login')
        data = {'username': 'admin@admin.com', 'password': 'admin'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'token')

    def test_logout(self):
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        url = reverse('accounts:logout')
        response = self.client.post(url, header={
            'Authorization': f'Token {token.key}'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
