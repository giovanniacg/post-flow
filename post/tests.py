from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from .models import Post
from status.models import Status
from address.models import Address
from django.contrib.auth.models import User
from django.test import override_settings

class PostViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.other_user = User.objects.create_user(username='otheruser', password='otherpassword')
        self.address = Address.objects.create(user=self.user, street='Test street', number='123',
                                              complement='Test complement', city='Test city', state='Test state',
                                              country='Test country', zip_code='12345')
        self.admin_user = User.objects.create_superuser(username='adminuser', password='adminpassword')

        self.status = Status.objects.create(name='Test status', description='Test description', order=0)
        self.other_status = Status.objects.create(name='Other status', description='Other description', order=1)

        self.post = Post.objects.create(user=self.user, current_status=self.status, address=self.address)
        self.other_post = Post.objects.create(user=self.other_user, current_status=self.status, address=self.address)
        self.total_posts = 2

        self.client.force_authenticate(user=self.user)

        self.post_urls = {
            'list': reverse('post-list'),
            'create': reverse('post-list'),
            'detail': reverse('post-detail', kwargs={'pk': self.post.pk}),
        }

    def test_list_posts_as_unauthenticated_user(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.post_urls['list'])
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}})
    def test_list_posts_as_user(self):
        response = self.client.get(self.post_urls['list'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user'], self.user.pk)

    @override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}})
    def test_list_posts_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.post_urls['list'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), self.total_posts)

    def test_create_post_as_user(self):
        data = {'user': self.user.pk, 'current_status_id': self.status.pk, 'address_id': self.address.pk}
        response = self.client.post(self.post_urls['create'], data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), self.total_posts + 1)

    def test_create_post_as_admin(self):
        data = {'user': self.user.pk, 'current_status_id': self.status.pk, 'address_id': self.address.pk}
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(self.post_urls['create'], data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), self.total_posts + 1)

    def test_retrieve_post_as_user(self):
        response = self.client.get(self.post_urls['detail'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.user.pk)

    def test_update_post_as_user(self):
        data = {'current_status_id': self.other_status.pk}
        response = self.client.patch(self.post_urls['detail'], data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.post.refresh_from_db()
        self.assertEqual(self.post.current_status, self.status)

    def test_update_post_as_admin(self):
        data = {'current_status_id': self.other_status.pk}
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.patch(self.post_urls['detail'], data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.current_status, self.other_status)

    def test_delete_post_as_user(self):
        response = self.client.delete(self.post_urls['detail'])
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.count(), self.total_posts)

    def test_delete_post_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.post_urls['detail'])
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), self.total_posts - 1)