from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from recipe.apps.core.models import Tag
from recipe.apps.recipes.serializers.recipe import TagSerializer
from recipe.apps.user.tests.test_user_api import create_user


User = get_user_model()

TAGS_URL = reverse('recipes:tag-list')


class PublicTagsApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        response = self.client.get(TAGS_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    def setUp(self):
        self.user: User = create_user(
            email='test@fernando.com',
            password='passwordtest',
            name='Test'
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_tags(self):
        Tag.objects.create(
            user=self.user,
            name="Vegano"
        )

        Tag.objects.create(
            user=self.user,
            name="Só come porqueira"
        )

        response = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')

        serializer = TagSerializer(tags, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_tags_limited_to_user(self):
        user_2: User = create_user(
            email='test2@fernando.com',
            password='passwordtest',
            name='Teste'
        )

        Tag.objects.create(
            user=user_2,
            name="Vegano"
        )

        tag = Tag.objects.create(
            user=self.user,
            name="Só come porqueira"
        )

        response = self.client.get(TAGS_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], tag.name)

    def test_create_tag_sucessful(self):
        payload = {
            'name': 'New tag'
        }

        response = self.client.post(TAGS_URL, payload)

        exists = Tag.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()

        self.assertTrue(exists)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_tag_invalid(self):
        payload = {
            'name': ''
        }

        response = self.client.post(TAGS_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
