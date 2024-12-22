from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

class UserViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.other_user = User.objects.create_user(username='otheruser', password='otherpassword')
        self.admin_user = User.objects.create_superuser(username='adminuser', password='adminpassword')
        self.total_users = 3

        self.client.force_authenticate(user=self.user)

        self.user_urls = {
            'list': reverse('user-list'),
            'create': reverse('user-list'),
            'detail-user': reverse('user-detail', kwargs={'pk': self.user.pk}),
            'detail-other': reverse('user-detail', kwargs={'pk': self.other_user.pk}),
            'detail-admin': reverse('user-detail', kwargs={'pk': self.admin_user.pk}),
        }

    def test_list_users_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.user_urls['list'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_users_as_non_admin(self):
        response = self.client.get(self.user_urls['list'])
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user(self):
        data = {'username': 'newuser', 'password': 'newpassword'}
        response = self.client.post(self.user_urls['create'], data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), self.total_users + 1)

    def test_retrieve_user_as_owner(self):
        response = self.client.get(self.user_urls['detail-user'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)

    def test_retrieve_user_as_non_owner(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(self.user_urls['detail-user'])
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_user_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.user_urls['detail-user'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_as_owner(self):
        data = {'username': 'updateduser'}
        response = self.client.patch(self.user_urls['detail-user'], data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')

    def test_update_user_as_non_owner(self):
        self.client.force_authenticate(user=self.other_user)
        data = {'username': 'updateduser'}
        response = self.client.patch(self.user_urls['detail-user'], data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_user_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {'username': 'updateduser'}
        response = self.client.patch(self.user_urls['detail-user'], data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')

    def test_delete_user_as_owner(self):
        response = self.client.delete(self.user_urls['detail-user'])
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), self.total_users - 1)

    def test_delete_user_as_non_owner(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(self.user_urls['detail-user'])
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(User.objects.count(), self.total_users)

    def test_delete_user_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.user_urls['detail-user'])
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), self.total_users - 1)