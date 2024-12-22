from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from .models import Status  # Assuming you have a Status model in status/models.py
from django.contrib.auth.models import User

class StatusViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.admin_user = User.objects.create_superuser(username='adminuser', password='adminpassword')

        self.status = Status.objects.create(name='Test status', description="Test description", order=0)
        self.total_status = 1

        self.client.force_authenticate(user=self.user)

        self.status_urls = {
            'list': reverse('status-list'),
            'create': reverse('status-list'),
            'detail': reverse('status-detail', kwargs={'pk': self.status.pk}),
        }

    def test_list_status_as_unauthenticated_user(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.status_urls['list'])
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_status_as_user(self):
        response = self.client.get(self.status_urls['list'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_status_as_user(self):
        data = {'name': 'New status', 'description': 'New description', 'order': 1}
        response = self.client.post(self.status_urls['create'], data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Status.objects.count(), self.total_status)

    def test_create_status_as_admin(self):
        data = {'name': 'New status', 'description': 'New description', 'order': 1}
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(self.status_urls['create'], data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Status.objects.count(), self.total_status + 1)

    def test_retrieve_status_as_user(self):
        response = self.client.get(self.status_urls['detail'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.status.name)

    def test_update_status_as_user(self):
        data = {'name': 'Updated status'}
        response = self.client.patch(self.status_urls['detail'], data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Test status')

    def test_update_status_as_admin(self):
        data = {'name': 'Updated status'}
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.patch(self.status_urls['detail'], data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Updated status')

    def test_delete_status_as_user(self):
        response = self.client.delete(self.status_urls['detail'])
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Status.objects.count(), self.total_status)

    def test_delete_status_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.status_urls['detail'])
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Status.objects.count(), self.total_status - 1)