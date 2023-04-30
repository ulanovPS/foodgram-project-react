from djoser.views import UserViewSet
from rest_framework import mixins, viewsets, permissions

from grocery_assistant.models import Ingredients, Tags
from users.models import User

from .paginations import CustomPagination
from .serializers import IngredientsSerializer, TagsSerializer, CustomUserSerializer


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
