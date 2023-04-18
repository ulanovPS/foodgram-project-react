from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe

from .models import *

admin.site.unregister(User) # Отменяем для панели администрирования

@admin.register(User) # Добавляем поля для поиска в модель User
class CustomUserAdmin(UserAdmin):
    list_filter = ('username', 'email', )
    search_fields = ('username', 'email', )

class UninAdmin(admin.ModelAdmin):
    list_display = ('pk', 'unit_name',)
    search_fields = ('unit_name',)
    list_filter  = ('unit_name',)

class RecipesAdmin(admin.ModelAdmin):
    list_filter = ('recipe_name',)
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

    def get_photo(self, object):
        if object.image:
            return mark_safe(f"<img src='{object.image.url}' width=50>")
    get_photo.short_description = "Миниатюра"

    def get_count_favorite(self, object):
        from django.db.models import Count
        count = Favorite_recipes.objects.filter(recipes_id=object).count()
        return f'{count} Раз'
    get_count_favorite.short_description = 'Добавили в избранное'

class FavoriteRecipesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user_id', 'recipes_id')

admin.site.site_header = 'Админ-панель сайта рецетов'
admin.site.site_title = 'Админ-панель сайта рецетов'

admin.site.register(Recipes, RecipesAdmin)
admin.site.register(Tags)
admin.site.register(Tags_list)
admin.site.register(Unit_of_measure, UninAdmin)
admin.site.register(Ingredients)
admin.site.register(Ingredients_list)
admin.site.register(Shoping_list)
admin.site.register(Favorite_recipes, FavoriteRecipesAdmin)
admin.site.register(Follow)