from djoser.views import UserViewSet
from rest_framework import mixins, permissions, viewsets

from grocery_assistant.models import Ingredients, Recipes, Tags
from users.models import User

from .paginations import CustomPagination
from .serializers import (IngredientsSerializer, RecipesSerializer,
                          TagsSerializer, UserSerializer)

from api.permissions import GuestIsReadOnlyAdminOrUserFullAccess


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class UserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination
    permission_classes = (GuestIsReadOnlyAdminOrUserFullAccess, )


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer
    pagination_class = CustomPagination


"""
    def get_serializer_class(self):
        print(self.request.method)
        if self.request.method in SAFE_METHODS:
            return RecipesSerializerList
        return
"""
