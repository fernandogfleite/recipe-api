from django.urls import (
    path,
    include
)

from rest_framework.routers import DefaultRouter

from recipe.apps.recipes.views import recipe

router = DefaultRouter()
router.register('tags', recipe.TagViewSet)
router.register('ingredients', recipe.IngredientViewSet)
router.register('recipes', recipe.RecipeViewSet)

app_name = 'recipes'

urlpatterns = [
    path(
        '', include(router.urls)
    )
]
