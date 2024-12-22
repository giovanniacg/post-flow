# base_tests.py
from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase
from address.models import Address
from status.models import Status
from post.models import Post

class BaseAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'password')
        self.user = User.objects.create_user('user', 'user@example.com', 'password')
        self.other_user = User.objects.create_user('other', 'other@example.com', 'password')

        self.address = Address.objects.create(
            street='123 Main St', number='1', complement='Apt 1', city='Anytown',
            state='Anystate', country='Anycountry', zip_code='12345', user=self.user
        )

        self.other_address = Address.objects.create(
            street='456 Elm St', number='2', complement='Apt 2', city='Othertown',
            state='Otherstate', country='Othercountry', zip_code='54321', user=self.other_user
        )

        self.status = Status.objects.create(name='Test status', description='Test description', order=0)
        self.other_status = Status.objects.create(name='Other status', description='Other description', order=1)

        self.post = Post.objects.create(user=self.user, status=self.status, address=self.address)
        self.other_post = Post.objects.create(user=self.other_user, status=self.status, address=self.other_address)