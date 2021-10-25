from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            email='test@fernando.com',
            password='test123'
        )
        self.client.force_login(self.admin_user)

        self.user = User.objects.create_user(
            email='test123@fernando.com',
            password='123test',
            name='Fernando Test'
        )

    def test_users_listed(self):
        url = reverse('admin:core_user_changelist')
        response = self.client.get(url)

        self.assertContains(response, self.user.name)
        self.assertContains(response, self.user.email)
