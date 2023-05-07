from rest_framework import status
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response

from api.filters import IngredientSearchFilter, RecipeFilter
from api.permissions import (GuestIsReadOnlyAdminOrOwnerFullAccess,
                             GuestIsReadOnlyAdminOrUserFullAccess)
from grocery_assistant.models import (Favorite_recipes, Ingredients, Recipes,
                                      Tags)
from users.models import User

from .paginations import CustomPagination
from .serializers import (CustomUserSerializer, IngredientsSerializer,
                          RecipesSerializerAdd, RecipesSerializerList,
                          TagsSerializer, FavoriteRecipesSerializer)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    search_fields = ('^ingr_name',)


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CustomPagination
    permission_classes = (GuestIsReadOnlyAdminOrOwnerFullAccess, )

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


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializerList
    pagination_class = CustomPagination
    permission_classes = (GuestIsReadOnlyAdminOrUserFullAccess, )

    def get_serializer_class(self):
        print(self.request.method)
        if self.request.method in SAFE_METHODS:
            return RecipesSerializerList
        return RecipesSerializerAdd

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

    def perform_destroy(self, serializer):
        serializer.delete(user_id=self.request.user)


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
