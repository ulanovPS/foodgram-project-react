from django.shortcuts import get_object_or_404
from djoser.serializers import SetPasswordSerializer
from djoser.views import UserViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response


from api.filters import IngredientNameFilter, RecipeFilter
from api.permissions import (GuestIsReadOnlyAdminOrOwnerFullAccess,
                             GuestIsReadOnlyAdminOrUserFullAccess)
from grocery_assistant.models import (Favorite_recipes, Follow, Ingredients,
                                      Recipes, Shoping_list, Tags, User)
from users.models import User

from .additions import download_product
from .paginations import CustomPagination
from .serializers import (CustomUserSerializer, FavoriteRecipesSerializer,
                          FollowRecipesSerializer, IngredientsSerializer,
                          RecipesSerializerAdd, RecipesSerializerList,
                          ShopingListSerializer, TagsSerializer)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (IngredientNameFilter, )
    search_fields = ('^ingr_name',)


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CustomPagination
    permission_classes = (GuestIsReadOnlyAdminOrUserFullAccess, )

    @action(detail=False,
            methods=['get'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        user = self.request.user
        serializer = CustomUserSerializer(user, context={'request': request})
        return Response(serializer.data)

    def get_permissions(self):
        # Если в GET-запросе требуется получить информацию об объекте
        if self.action == 'retrieve':
            # Вернем обновленный перечень используемых пермишенов
            return (IsAuthenticated(),)
        # Для остальных ситуаций оставим без изменений
        return super().get_permissions()

    @action(["post"],
            detail=False,
            permission_classes=[IsAuthenticated])
    def set_password(self, request, *args, **kwargs):
        """
        Кастомное изменение пароля с помощью cериалайзера
        из пакета djoser SetPasswordSerializer.
        """
        serializer = SetPasswordSerializer(
            data=request.data,
            context={'request': request})
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
        """Создание и удаление подписки."""
        author = get_object_or_404(User, id=self.kwargs.get('id'))
        user = self.request.user
        if request.method == 'POST':
            if not Follow.objects.filter(author=author, user_id=user).exists():
                serializer = FollowRecipesSerializer(
                    data=request.data,
                    context={'request': request, 'author': author}
                )
                if serializer.is_valid(raise_exception=True):
                    serializer.save(author=author, user_id=user)
                    return Response(
                        {'Подписка успешно создана': serializer.data},
                        status=status.HTTP_201_CREATED
                    )
                return Response({'errors': 'Объект не найден'},
                                status=status.HTTP_404_NOT_FOUND)
            return Response({'errors': 'Подписка уже создана'},
                            status=status.HTTP_404_NOT_FOUND)
        elif request.method == 'DELETE':
            if Follow.objects.filter(author=author, user_id=user).exists():
                val_count = Follow.objects.filter(author=author,
                                                  user_id=user).count()
                if val_count == 1:
                    Follow.objects.get(author=author).delete()
                    return Response('Успешная отписка',
                                    status=status.HTTP_204_NO_CONTENT)
                return Response({'errors': 'Системная ошибка'},
                                status=status.HTTP_404_NOT_FOUND)
            return Response({'errors': 'Объект не найден'},
                            status=status.HTTP_404_NOT_FOUND)

    @action(detail=False,
            methods=['get'],
            permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        """Отображает все подписки пользователя."""
        follows = Follow.objects.filter(user_id=self.request.user)
        pages = self.paginate_queryset(follows)
        serializer = FollowRecipesSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        self.get_paginated_response(serializer.data)
        return self.get_paginated_response(serializer.data)


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializerList
    pagination_class = CustomPagination
    permission_classes = (GuestIsReadOnlyAdminOrOwnerFullAccess, )
    # filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        print(self.request.method)
        if self.request.method in SAFE_METHODS:
            return RecipesSerializerList
        return RecipesSerializerAdd

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipes, id=self.kwargs.get('pk'))
        user = self.request.user
        if request.method == 'POST':
            if Favorite_recipes.objects.filter(user_id=user,
                                               recipes_id=recipe).exists():
                return Response({'errors': 'Рецепт уже в избранном!'},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer = FavoriteRecipesSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user_id=user, recipes_id=recipe)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        if not Favorite_recipes.objects.filter(user_id=user,
                                               recipes_id=recipe).exists():
            return Response({'errors': 'Рецепт уже удален из избранного!'},
                            status=status.HTTP_404_NOT_FOUND)
        Favorite_recipes.objects.get(recipes_id=recipe).delete()
        return Response('Рецепт успешно удалён из избранного.',
                        status=status.HTTP_204_NO_CONTENT)

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, *args, **kwargs):
        """
        Получить / Добавить / Удалить  рецепт
        из списка покупок у текущего пользоватля.
        """
        recipe = get_object_or_404(Recipes, id=self.kwargs.get('pk'))
        user = self.request.user
        if request.method == 'POST':
            if Shoping_list.objects.filter(user_id=user,
                                           recipes_id=recipe).exists():
                return Response({'errors': 'Рецепт уже добавлен!'},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer = ShopingListSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user_id=user, recipes_id=recipe)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'DELETE':
            if not Shoping_list.objects.filter(user_id=user,
                                               recipes_id=recipe).exists():
                return Response({'errors': 'Объект не найден'},
                                status=status.HTTP_404_NOT_FOUND)
            Shoping_list.objects.get(recipes_id=recipe).delete()
            return Response('Рецепт успешно удалён из списка покупок.',
                            status=status.HTTP_204_NO_CONTENT)

    @action(detail=False,
            methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        # Скачать список покупок для выбранных рецептов,данные суммируются.
        if Shoping_list.objects.filter(user_id=self.request.user.pk).exists():
            author = User.objects.get(id=self.request.user.pk)
            return download_product(self, request, author)
        return Response('Список покупок пуст.',
                        status=status.HTTP_404_NOT_FOUND)
