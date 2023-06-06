from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db.models.expressions import Exists, OuterRef, Value
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action, api_view
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
    UserCreateSerializer,
    UserPasswordSerializer,
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
        return Response({'token': token.key},
            status=status.HTTP_201_CREATED)


@api_view(['post'])
def set_password(request):
    """Изменить пароль."""
    serializer = UserPasswordSerializer(
        data=request.data,
        context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(
            {'message': 'Пароль изменен!'},
            status=status.HTTP_201_CREATED)
    return Response(
        {'error': 'Введите верные данные!'},
        status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(UserViewSet):
    """
    Пользователи и подписки.
    """
    serializer_class = UserSerializer
    pagination_class = LimitPageNumberPagination
    search_fields = ('username', 'email')
    permission_classes = (AllowAny,)

    def get_queryset(self):
        """ Получить список пользователей. """
        if self.request.user.is_authenticated:
            return (User.objects.annotate(is_subscribed=Exists(
                self.request.user.subscriber.filter(author=OuterRef('id'))))
                .prefetch_related('subscriber', 'subscribing'))
        return User.objects.annotate(is_subscribed=Value(False))

    def get_serializer_class(self):
        if self.request.method.lower() == 'post':
            return UserCreateSerializer
        return UserSerializer

    def perform_create(self, serializer):
        """ Создание пароля в формате postres. """
        password = make_password(self.request.data['password'])
        serializer.save(password=password)

    @action(methods=['POST', 'DELETE'],
            detail=True,
            permission_classes=(IsAuthenticated),)
    def subscribe(self, request, author_id):
        """ Добавляет и удаляет пользователей в подписчики. """
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
            self.paginate_queryset(Subscribe.objects.filter(
                                   user=request.user)),
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
    serializer_class = RecipeSerializer
    pagination_class = LimitPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = RecipeFilter
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,)

    def new_favorite_or_cart(self, model, user, pk):
        if model.objects.filter(user=user, recipe__id=pk).exists():
            return Response({'errors': 'Рецепт уже добавлен!'},
                            status=status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(RecipeList, recipe__id=pk)
        model.objects.create(user=user)
        serializer = FavoriteOrSubscribeSerializer(recipe, is_favorited=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def remove_favorite_or_cart(self, model, user, pk):
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'Рецепт уже удален!'},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST', 'DELETE'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None)
        """
        Добавить рецепт в избранное или удалить из него.
        """
        if request.method == 'POST':
            return self.new_favorite_or_cart(FavoriteRecipe,
                                             request.user, pk)
        return self.remove_favorite_or_cart(FavoriteRecipe,
                                            request.user, pk)

    @action(detail=True, methods=['POST', 'DELETE'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        """
        Добавить рецепт в список покупок или удалить из него.
        """
        if request.method == 'POST':
            return self.new_favorite_or_cart(ShoppingCart, request.user, pk)
        return self.remove_favorite_or_cart(ShoppingCart, request.user, pk)

    @action(detail=False, methods=['GET'],
            permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        """
        Скачать корзину (список) покупок.
        """
        response = HttpResponse(collect_shopping_cart(request.user),
                                content_type='text/plain')
        response['Content-Disposition'] = (
            'attachment; filename="shopping_cart.txt"')
        return response
