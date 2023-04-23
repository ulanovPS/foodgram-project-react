from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from .models import (Favorite_recipes, Follow, Ingredients, Ingredients_list,
                     Recipes, Shoping_list, Tags, Tags_list, Unit_of_measure)

admin.site.unregister(User)  # Отменяем для панели администрирования


@admin.register(User)  # Добавляем поля для поиска в модель User
class CustomUserAdmin(UserAdmin):
    list_filter = ('username', 'email', )
    search_fields = ('username', 'email', )


class RecipesTagListFilter(admin.SimpleListFilter):
    title = ('Поиск по тегам')
    parameter_name = "pk"

    def lookups(self, request, model_admin):
        if Tags.objects.exists:
            lst = []
            for i in Tags.objects.all():
                lst = lst + [((i.pk), _(i.tag_name),)]
            return lst
        else:
            pass

    def queryset(self, request, queryset):
        tag_id = self.value()
        if tag_id:
            return queryset.filter(tags_list__tag_id=tag_id)
        return queryset


class UninAdmin(admin.ModelAdmin):
    list_display = ('pk', 'unit_name',)
    search_fields = ('unit_name',)
    list_filter = ['unit_name', RecipesTagListFilter]


class RecipesAdmin(admin.ModelAdmin):
    list_filter = ['recipe_name', 'user_id__username', RecipesTagListFilter]
    list_display = (
        'pk',
        'recipe_name',
        'get_count_favorite',
        'user_id',
        'get_photo',
        'description',
        'cooking_time',
        'public_date'
    )
    fields = (
        'recipe_name',
        'user_id',
        'image',
        'get_photo',
        'description',
        'cooking_time',
        'public_date'
    )
    readonly_fields = ('public_date', 'get_photo')
    save_on_top = True
    empty_value_display = '-пусто-'
    ordering = ['pk', 'recipe_name']

    def get_photo(self, object):
        if object.image:
            return mark_safe(f"<img src='{object.image.url}' width=50>")
    get_photo.short_description = "Миниатюра"

    def get_count_favorite(self, object):
        count = Favorite_recipes.objects.filter(recipes_id=object).count()
        if count > 0:
            return f'{count} Пользователь'
        else:
            return '-'
    get_count_favorite.short_description = 'Добавили в избранное'


class FavoriteRecipesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user_id', 'recipes_id')


class IngredientsAdmin(admin.ModelAdmin):
    list_filter = ('ingr_name',)
    list_display = ('pk', 'ingr_name', 'get_unit_of_measure',)
    readonly_fields = ('get_unit_of_measure',)

    def get_unit_of_measure(self, object):

        try:
            get_object_or_404(Ingredients_list, ingr_id=object)
            unit = Ingredients_list.objects.filter(
                ingr_id=object
            ).select_related('unit_id')
            string = ''
            for i in unit:
                string = string + i.unit_id.unit_name
            return string
        except Exception:
            return '-'

    get_unit_of_measure.short_description = 'Единицы измерения'


class TagsAdmin(admin.ModelAdmin):
    list_display = ['pk', 'tag_name', 'color', 'slug']


class TagsListAdmin(admin.ModelAdmin):
    list_display = ['pk', 'tag_id', 'recipes_id']


class Ingredients_listAdmin(admin.ModelAdmin):
    list_display = ['recipes_id', 'ingr_id', 'unit_id']


admin.site.site_header = 'Админ-панель сайта рецетов'
admin.site.site_title = 'Админ-панель сайта рецетов'

admin.site.register(Recipes, RecipesAdmin)
admin.site.register(Tags, TagsAdmin)
admin.site.register(Tags_list, TagsListAdmin)
admin.site.register(Unit_of_measure, UninAdmin)
admin.site.register(Ingredients, IngredientsAdmin)
admin.site.register(Ingredients_list, Ingredients_listAdmin)
admin.site.register(Shoping_list)
admin.site.register(Favorite_recipes, FavoriteRecipesAdmin)
admin.site.register(Follow)
