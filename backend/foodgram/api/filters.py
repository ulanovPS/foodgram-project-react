from django_filters.rest_framework import FilterSet, filters
from rest_framework.filters import SearchFilter

from grocery_assistant.models import Recipes, Tags, User


class IngredientNameFilter(SearchFilter):
    search_param = 'name'


class RecipesFilter(FilterSet):
    author = filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        field_name='user_id'
    )
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tags.objects.all(),
    )
    is_in_shopping_cart = filters.NumberFilter(
        method='filter_is_in_shopping_cart')
    is_favorited = filters.NumberFilter(
        method='filter_is_favorited')

    class Meta:
        model = Recipes
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def filter_is_favorited(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(favorite__user_id=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(shoping_list__user_id=self.request.user)
        return queryset
