from api.permissions import (GuestIsReadOnlyAdminOrOwnerFullAccess,
                             GuestIsReadOnlyAdminOrUserFullAccess)
from djoser.views import UserViewSet
from grocery_assistant.models import Ingredients, Recipes, Tags
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from users.models import User

from .paginations import CustomPagination
from .serializers import (CustomUserSerializer, IngredientsSerializer,
                          RecipesSerializerAdd, RecipesSerializerList,
                          TagsSerializer)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


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
