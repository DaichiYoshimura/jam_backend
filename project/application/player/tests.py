from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class PlayerTests(APITestCase):

    def test_create_player(self):
        url = reverse('tune-list')
        request_data = {
            'name': ''
        }
        response = self.client.post(url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
