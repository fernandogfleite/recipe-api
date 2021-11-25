from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from recipe.apps.core.models import (
    Recipe,
    Tag,
    Ingredient
)

from recipe.apps.recipes.serializers.recipe import (
    RecipeSerializer,
    RecipeDetailSerializer
)
from recipe.apps.user.tests.test_user_api import create_user


User = get_user_model()

RECIPES_URL = reverse('recipes:recipe-list')


def detail_url(recipe_id: int) -> str:
    return reverse('recipes:recipe-detail', args=[recipe_id])


def sample_recipe(user: User, **params) -> Recipe:

    defaults = {
        'title': 'Peixada',
        'time_minutes': 5,
        'price': 5.00
    }

    defaults.update(params)

    return Recipe.objects.create(
        user=user,
        **defaults
    )


def sample_ingredient(user: User, name='Camarão') -> Ingredient:

    return Ingredient.objects.create(
        user=user,
        name=name
    )


def sample_tag(user: User, name='Frutos do mar') -> Tag:

    return Tag.objects.create(
        user=user,
        name=name
    )


class PublicRecipeApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(RECIPES_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user: User = create_user(
            email='test@fernando.com',
            password='passwordtest',
            name='Test'
        )

        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        sample_recipe(self.user)
        sample_recipe(self.user)

        response = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_recipes_limited_to_user(self):
        user_2 = create_user(
            email="testfernando@test.com",
            password='passwordtest',
            name='Testes'
        )
        sample_recipe(self.user)
        sample_recipe(user_2)

        response = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.filter(user=self.user).order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_recipe_detail(self):
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        recipe.ingredients.add(sample_ingredient(user=self.user))

        url = detail_url(recipe.id)

        response = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)

        self.assertEqual(response.data, serializer.data)
