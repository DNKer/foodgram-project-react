from django.contrib.auth import get_user_model
from django.db.models.expressions import Exists, OuterRef, Value
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import (
    ModelViewSet,
    ReadOnlyModelViewSet
)
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)

from .filters import IngredientFilter, RecipeFilter
from .pagination import LimitPageNumberPagination
from recipes.models import (
    FavoriteRecipe,
    Ingredient,
    RecipeList,
    ShoppingCart,
    Subscribe,
    Tag
)
from .serializers import (
    AuthSerializer,
    IngredientSerializer,
    FavoriteOrSubscribeSerializer,
    RecipeSerializer,
    SubscribeSerializer,
    TagSerializer,
    UserSerializer
)
from .services import collect_shopping_cart


User = get_user_model()


class AuthToken(ObtainAuthToken):
    """
    Авторизация пользователя.
    """

    serializer_class = AuthSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {'auth_token': token.key},
            status=status.HTTP_201_CREATED)


class UsersViewSet(UserViewSet):
    """
    Пользователи и подписки.
    """
    serializer_class = UserSerializer
    pagination_class = LimitPageNumberPagination

    def get_queryset(self):
        """ Получить список пользователей. """
        if self.request.user.is_authenticated:
            return (User.objects.annotate(is_subscribed=Exists(
                self.request.user.subscriber.filter(author=OuterRef('id'))
                )).prefetch_related('subscriber', 'subscribing'))
        return User.objects.annotate(is_subscribed=Value(False))

    @action(methods=['POST', 'DELETE'],
            detail=True,
            permission_classes=(IsAuthenticated),)
    def subscribe(self, request, author_id):
        """ Подписаться / отписаться. """
        author = get_object_or_404(User, id=author_id)
        queryset = Subscribe.objects.filter(user=request.user,
                                            author=author)
        if request.method == 'POST':
            serializer = SubscribeSerializer(
                Subscribe.objects.create(user=request.user, author=author),
                context={'request': request})
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        if queryset.exists():
            queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        """ Получить на кого пользователь подписан. """
        serializer = SubscribeSerializer(
            self.paginate_queryset(
                        Subscribe.objects.filter(user=request.user)),
            many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)


class TagsViewSet(ReadOnlyModelViewSet):
    """
    Список тэгов.
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientsViewSet(ReadOnlyModelViewSet):
    """
    Список ингридиентов.
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientFilter,)
    search_fields = ('^name',)
    pagination_class = None


class RecipesViewSet(ModelViewSet):
    """
    Список рецептов.
    """
    queryset = RecipeList.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = LimitPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = RecipeFilter
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,)

    def new_favorite_or_cart(self, model, user, pk):
        recipe = get_object_or_404(RecipeList, recipe__id=pk)
        model.objects.create(user=user)
        serializer = FavoriteOrSubscribeSerializer(recipe, is_favorited=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def remove_favorite_or_cart(self, model, user, pk):
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['POST', 'DELETE'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None) -> Response:
        """
        Добавить рецепт в избранное или удалить из него.
        """
        if request.method == 'POST':
            return self.new_favorite_or_cart(
                            FavoriteRecipe, request.user, pk)
        return self.remove_favorite_or_cart(
                            FavoriteRecipe, request.user, pk)

    @action(detail=True, methods=['POST', 'DELETE'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        """
        Добавить рецепт в список покупок или удалить из него.
        """
        if request.method == 'POST':
            return self.new_favorite_or_cart(
                            ShoppingCart, request.user, pk)
        return self.remove_favorite_or_cart(
                            ShoppingCart, request.user, pk)

    @action(detail=False, methods=['GET'],
            permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        """
        Скачать корзину (список) покупок.
        """
        response = HttpResponse(
                        collect_shopping_cart(request.user),
                        content_type='text/plain'
        )
        response['Content-Disposition'] = (
            'attachment; filename="shopping_cart.txt"')
        return response
