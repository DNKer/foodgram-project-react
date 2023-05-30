from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AuthToken,
    IngredientsViewSet,
    RecipesViewSet,
    set_password,
    TagsViewSet,
    UsersViewSet
)


app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register(
    'users',
    UsersViewSet,
    basename='users'
)
router_v1.register(
    'tags',
    TagsViewSet,
    basename='tags'
)
router_v1.register(
    'ingredients',
    IngredientsViewSet,
    basename='ingredients'
)
router_v1.register(
    'recipes',
    RecipesViewSet,
    basename='recipes'
)

urlpatterns = [
    path(
        'auth/token/login/',
        AuthToken.as_view(),
        name='login'),
    path("users/set_password/", set_password, name="set_password"),
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path(
        'auth/',
        include('djoser.urls.authtoken'),
        name='auth'),
]
