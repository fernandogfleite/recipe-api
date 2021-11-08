from django.urls import path

from recipe.apps.user.views.authentication import (
    UserView,
    CreateTokenView
)


app_name = 'user'

urlpatterns = [
    path(
        'create/',
        UserView.as_view(),
        name='create'
    ),
    path(
        'token/',
        CreateTokenView.as_view(),
        name='token'
    )
]
