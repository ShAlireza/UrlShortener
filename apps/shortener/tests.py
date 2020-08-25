from django.urls import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from apps.accounts.models import User
from .models import ShortenedURL


class ShortenedURLTests(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='admin',
                                             email='admin@admin.com',
                                             password='admin')
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

    def test_short_url_create(self):
        url = reverse('shortener:short_url')
        data = {'long_url': 'https://google.com', 'suggested_path': 'yektanet'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertContains(response, 'shortened_url',
                            status_code=status.HTTP_201_CREATED)
        shortened_url = ShortenedURL.objects.all().last()
        has_analytics = hasattr(shortened_url, 'analytic')
        self.assertEqual(has_analytics, True)

    def test_short_url_list(self):
        url = reverse('shortener:short_url')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_short_url_200_requests(self):
        url = reverse('shortener:short_url')
        data = {'long_url': 'https://google.com', 'suggested_path': 'yektanet'}

        for _ in range(200):
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertContains(response, 'shortened_url',
                                status_code=status.HTTP_201_CREATED)
        self.assertEqual(ShortenedURL.objects.count(), 200)
