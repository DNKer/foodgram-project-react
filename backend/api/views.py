from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from .filters import IngredientFilter, TagsFilter, RecipeFilter
from .pagination import LimitPageNumberPagination
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from recipes.models import (
    FavoriteRecipe,
    Ingredient,
    RecipeList,
    ShoppingCart,
    Tag
)
from .serializers import (
    IngredientSerializer,
    FavoriteOrSubscribeSerializer,
    RecipeSerializer,
    SubscribeSerializer,
    TagSerializer,
    UserPasswordSerializer
)
from .services import collect_shopping_cart
from users.models import Subscribe


User = get_user_model()


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


class UserViewSet(DjoserUserViewSet):
    """
    Пользователи и подписки.
    """
    lookup_url_kwarg = 'author_id'

    @action(methods=['POST', 'DELETE'], detail=True,)
    def subscribe(self, request, author_id):
        author = get_object_or_404(User, id=author_id)
        if request.method == 'POST':
            if request.user.id == author.id:
                raise ValueError('Нельзя подписаться на себя самого')
            serializer = SubscribeSerializer(
                Subscribe.objects.create(user=request.user, author=author),
                context={'request': request})
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if Subscribe.objects.filter(user=request.user,
                                        author=author
                                        ).exists():
                Subscribe.objects.filter(user=request.user,
                                         author=author
                                         ).delete()
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
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = (TagsFilter,)
    pagination_class = None


class IngredientsViewSet(ReadOnlyModelViewSet):
    """
    Список ингридиентов.
    """
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientFilter,)
    search_fields = ('^name',)
    pagination_class = None


class RecipesViewSet(viewsets.ModelViewSet):
    """
    Список рецептов.
    """
    serializer_class = RecipeSerializer
    pagination_class = LimitPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = RecipeFilter
    permission_classes = (IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,)

    def new_favorite_or_cart(self, model, user, pk):
        if model.objects.filter(user=user, recipe__id=pk).exists():
            return Response({'errors': 'Рецепт уже добавлен!'},
                            status=status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(RecipeList, recipe__id=pk)
        model.objects.create(user=user, recipe=recipe)
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
    def favorite(self, request, pk=None):
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
