from django.urls import path

from recipe.apps.user.views.authentication import (
    UserView,
    CreateTokenView,
    ManagerUserView
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
    ),
    path(
        'me/',
        ManagerUserView.as_view(),
        name='me'
    )
]
