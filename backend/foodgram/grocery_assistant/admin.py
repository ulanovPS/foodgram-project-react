from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from .models import (Favorite_recipes, Follow, Ingredients, Ingredients_list,
                     Recipes, Shoping_list, Tags, Tags_list)


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
    list_display = ('pk', 'ingr_name', 'measurement_unit',)


class TagsAdmin(admin.ModelAdmin):
    list_display = ['pk', 'tag_name', 'color', 'slug']


class TagsListAdmin(admin.ModelAdmin):
    list_display = ['pk', 'tag_id', 'recipes_id']


class Ingredients_listAdmin(admin.ModelAdmin):
    list_display = ['recipes_id', 'ingr_id', 'quantity']


admin.site.site_header = 'Админ-панель сайта рецетов'
admin.site.site_title = 'Админ-панель сайта рецетов'

admin.site.register(Recipes, RecipesAdmin)
admin.site.register(Tags, TagsAdmin)
admin.site.register(Tags_list, TagsListAdmin)
admin.site.register(Ingredients, IngredientsAdmin)
admin.site.register(Ingredients_list, Ingredients_listAdmin)
admin.site.register(Shoping_list)
admin.site.register(Favorite_recipes, FavoriteRecipesAdmin)
admin.site.register(Follow)
