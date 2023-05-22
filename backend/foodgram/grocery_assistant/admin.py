from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from .models import (FavoriteRecipe, Follow, Ingredient, IngredientRecipe,
                     Recipe, ShopingList, Tag)


class IngredientsInline(admin.TabularInline):
    model = IngredientRecipe
    extra = 3


class RecipesTagListFilter(admin.SimpleListFilter):
    title = ('Поиск по тегам')
    parameter_name = "pk"

    def lookups(self, request, model_admin):
        if Tag.objects.exists:
            lst = []
            for i in Tag.objects.all():
                lst = lst + [((i.pk), _(i.name),)]
            return lst
        return '-'

    def queryset(self, request, queryset):
        tag_id = self.value()
        if tag_id:
            return queryset.filter(tags_list__tag_id=tag_id)
        return queryset


class RecipeAdmin(admin.ModelAdmin):
    list_filter = ['name', 'author__username', 'tags']
    list_display = (
        'pk',
        'name',
        'get_count_favorite',
        'author',
        'get_photo',
        'description',
        'cooking_time',
        'pub_date',
        'get_products',
    )
    fields = (
        'name',
        'author',
        'image',
        'get_photo',
        'description',
        'cooking_time',
        'pub_date',
        'tags',
    )
    readonly_fields = ('pub_date', 'get_photo')
    save_on_top = True
    empty_value_display = '-пусто-'
    ordering = ['pk', 'name']
    inlines = [IngredientsInline]

    def get_products(self, obj):
        return "\n".join([p.name for p in obj.tags.all()])

    def get_photo(self, object):
        if object.image:
            return mark_safe(f"<img src='{object.image.url}' width=50>")
        return
    get_photo.short_description = "Миниатюра"

    def get_count_favorite(self, object):
        count = FavoriteRecipe.objects.filter(recipes=object).count()
        if count > 0:
            return f'{count} Пользователь'
        return '-'
    get_count_favorite.short_description = 'Добавили в избранное'


class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipes')


class IngredientAdmin(admin.ModelAdmin):
    list_filter = ('name',)
    list_display = ('pk', 'name', 'measurement_unit',)


class TagAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'color', 'slug']
    list_filter = ('name',)
    search_fields = ('name',)


class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = ['recipes', 'ingredient', 'amount']


class FollowAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'author']


class ShopingListAdmin(admin.ModelAdmin):
    list_display = ['user', 'recipes']


admin.site.site_header = 'Админ-панель сайта рецетов'
admin.site.site_title = 'Админ-панель сайта рецетов'

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientRecipe, IngredientRecipeAdmin)
admin.site.register(ShopingList, ShopingListAdmin)
admin.site.register(FavoriteRecipe, FavoriteRecipeAdmin)
admin.site.register(Follow, FollowAdmin)
