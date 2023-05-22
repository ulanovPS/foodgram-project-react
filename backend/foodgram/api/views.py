from api.filters import IngredientNameFilter, RecipesFilter
from api.permissions import GuestIsReadOnlyAdminOrOwnerFullAccess
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.serializers import SetPasswordSerializer
from djoser.views import UserViewSet
from grocery_assistant.models import (FavoriteRecipe, Follow, Ingredient,
                                      Recipe, ShopingList, Tag, User)
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from users.models import User

from .additions import download_product
from .paginations import CustomPagination
from .serializers import (CustomUserSerializer, FavoriteRecipesSerializer,
                          FollowRecipesSerializer, IngredientsSerializer,
                          RecipesSerializerAdd, RecipesSerializerList,
                          ShopingListSerializer, TagsSerializer)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    """ View отображение тегов, методы List и Retrieve"""
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    """ View отображение ингридиентов, методы List и Retrieve"""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (IngredientNameFilter, )
    search_fields = ('^name',)  # Поиск по имени ингридиента


class CustomUserViewSet(UserViewSet):
    """ View отображение пользователей """
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CustomPagination
    (permissions.IsAuthenticatedOrReadOnly,)

    @action(detail=False,
            methods=['get'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        """ Получение данных текущего пользователя """
        user = self.request.user
        serializer = CustomUserSerializer(user, context={'request': request})
        return Response(serializer.data)

    def get_permissions(self):
        """ Переопредиляем права доступа """
        if self.action == 'retrieve':
            return (IsAuthenticated(),)
        return super().get_permissions()

    @action(["post"],
            detail=False,
            permission_classes=[IsAuthenticated])
    def set_password(self, request, *args, **kwargs):
        """ Произвольное изменение паролья """
        serializer = SetPasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            self.request.user.set_password(serializer.data["new_password"])
            self.request.user.save()
            return Response('Пароль успешно изменен',
                            status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, *args, **kwargs):
        """Создание и удаление подписки """
        author = get_object_or_404(User, id=self.kwargs.get('id'))
        user = self.request.user
        if request.method == 'POST':
            if not Follow.objects.filter(author=author, user=user).exists():
                serializer = FollowRecipesSerializer(
                    data=request.data,
                    context={'request': request, 'author': author}
                )
                if serializer.is_valid(raise_exception=True):
                    serializer.save(author=author, user=user)
                    return Response(
                        {'Подписка успешно создана': serializer.data},
                        status=status.HTTP_201_CREATED
                    )
                return Response({'errors': 'Объект не найден'},
                                status=status.HTTP_404_NOT_FOUND)
            return Response({'errors': 'Подписка уже создана'},
                            status=status.HTTP_404_NOT_FOUND)
        elif request.method == 'DELETE':
            if Follow.objects.filter(author=author, user=user).exists():
                Follow.objects.get(author=author,
                                   user=user).delete()
                return Response('Успешная отписка',
                                status=status.HTTP_204_NO_CONTENT)
            return Response({'errors': 'Объект не найден'},
                            status=status.HTTP_404_NOT_FOUND)

    @action(detail=False,
            methods=['get'],
            permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        """Отображаем все подписки пользователя """
        follows = Follow.objects.filter(user=self.request.user)
        pages = self.paginate_queryset(follows)
        serializer = FollowRecipesSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        self.get_paginated_response(serializer.data)
        return self.get_paginated_response(serializer.data)


class RecipesViewSet(viewsets.ModelViewSet):
    """ View отображение рецептов """
    queryset = Recipe.objects.all()
    serializer_class = RecipesSerializerList
    pagination_class = CustomPagination
    permission_classes = (GuestIsReadOnlyAdminOrOwnerFullAccess, )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipesFilter

    def get_serializer_class(self):
        """ Выбираем какой сериализатор использовать """
        if self.request.method in SAFE_METHODS:
            return RecipesSerializerList  # Для отображения списка
        return RecipesSerializerAdd  # Для добавления и редакирования

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, *args, **kwargs):
        """" Создаем и удаляем рецепт из избранного """
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('pk'))
        user = self.request.user
        if request.method == 'POST':
            if FavoriteRecipe.objects.filter(user=user,
                                             recipes=recipe).exists():
                return Response({'errors': 'Рецепт уже в избранном!'},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer = FavoriteRecipesSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user, recipes=recipe)
        if not FavoriteRecipe.objects.filter(user=user,
                                             recipes=recipe).exists():
            return Response({'errors': 'Рецепт уже удален из избранного!'},
                            status=status.HTTP_404_NOT_FOUND)
        FavoriteRecipe.objects.get(recipes=recipe).delete()
        return Response('Рецепт успешно удалён из избранного.',
                        status=status.HTTP_204_NO_CONTENT)

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, *args, **kwargs):
        """ Создаем и удаляем рецепт в список покупок """
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('pk'))
        user = self.request.user
        if request.method == 'POST':
            if ShopingList.objects.filter(user=user,
                                          recipes=recipe).exists():
                return Response({'errors': 'Рецепт уже добавлен!'},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer = ShopingListSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=user, recipes=recipe)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'DELETE':
            if not ShopingList.objects.filter(user=user,
                                              recipes=recipe).exists():
                return Response({'errors': 'Объект не найден'},
                                status=status.HTTP_404_NOT_FOUND)
            ShopingList.objects.get(recipes=recipe).delete()
            return Response('Рецепт успешно удалён из списка покупок.',
                            status=status.HTTP_204_NO_CONTENT)

    @action(detail=False,
            methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        """ Скачать список полкупок """
        if ShopingList.objects.filter(user=self.request.user.pk).exists():
            author = User.objects.get(id=self.request.user.pk)
            return download_product(self, request, author)
        return Response('Список покупок пуст.',
                        status=status.HTTP_404_NOT_FOUND)
