from django.core import exceptions
from django.core.validators import MinValueValidator
from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from grocery_assistant.models import (COLOR_TAG, Favorite_recipes, Follow,
                                      Ingredients, Ingredients_list, Recipes,
                                      Shoping_list, Tags)
from users.models import User


class TagsSerializer(serializers.ModelSerializer):
    """ Сериализатор тегов """
    name = serializers.CharField(source='tag_name')
    color = serializers.ChoiceField(choices=COLOR_TAG)

    class Meta:
        fields = ('id', 'name', 'color', 'slug')
        model = Tags


class IngredientsSerializer(serializers.ModelSerializer):
    """ Сериализатор ингридиентов """
    name = serializers.CharField(source='ingr_name')

    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredients


class CustomUserSerializer(UserSerializer):
    """ Сериализатор пользователя """
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
            'is_subscribed'
        )
        extra_kwargs = {'password': {'write_only': True},
                        'is_subscribed': {'read_only': True}}

    def get_is_subscribed(self, obj):
        """ Подписан ли текущий пользователь на выбранного """
        user = self.context.get('request').user
        if not user.is_anonymous:
            return Follow.objects.filter(user_id=user, author=obj).exists()
        return False

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class Ingredients_listSerializer(serializers.ModelSerializer):
    """ Вложеные сериализатор отображения рецептов """
    id = serializers.ReadOnlyField(
        source='ingr_id.id'
    )
    name = serializers.ReadOnlyField(
        source='ingr_id.ingr_name'
    )
    measurement_unit = serializers.ReadOnlyField(
        source='ingr_id.measurement_unit'
    )
    amount = serializers.IntegerField(
        source='quantity'
    )

    class Meta:
        model = Ingredients_list
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipesSerializerList(serializers.ModelSerializer):
    """ Сериализатор отображения рецептов """
    text = serializers.StringRelatedField(
        read_only=True,
        source='description'
    )
    name = serializers.StringRelatedField(
        read_only=True,
        source='recipe_name'
    )
    tags = TagsSerializer(read_only=True, many=True)
    is_in_shopping_cart = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    author = CustomUserSerializer(source='user_id')
    ingredients = Ingredients_listSerializer(
        many=True,
        source='recipes_list',
        read_only=True
    )

    class Meta:
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )
        model = Recipes

    def get_is_in_shopping_cart(self, obj):
        """ Добавлен ли рецепт в список покупок True/False """
        user = self.context.get('request').user
        if not user.is_anonymous:
            return Shoping_list.objects.filter(
                recipes_id=obj,
                user_id=user.id
            ).exists()
        return False

    def get_is_favorited(self, obj):
        """ Добавлен ли рецепт в избранное True/False """
        user = self.context.get('request').user
        if not user.is_anonymous:
            return Favorite_recipes.objects.filter(
                recipes_id=obj,
                user_id=user.id
            ).exists()
        return False


class AddIngredientsSerializer(serializers.ModelSerializer):
    """ Вложеный сериализатор добавления нового рецепта """
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredients.objects.all(),
        source='ingr_id'
    )
    amount = serializers.IntegerField(
        source='quantity',
        validators=(
            MinValueValidator(
                1,
                message='Минимальное значение >= 1'
            ),  # Проверка для значения кол-ва ингридиента
        ),
    )

    class Meta:
        model = Ingredients_list
        fields = ('id', 'amount')


class RecipesSerializerAdd(serializers.ModelSerializer):
    """ Сериализатор добавления рецепта """
    ingredients = AddIngredientsSerializer(
        many=True,
        source='recipes_list'
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tags.objects.all(),
        many=True,
    )
    image = Base64ImageField()
    text = serializers.CharField(
        source='description',
    )
    name = serializers.CharField(
        source='recipe_name'
    )
    author = CustomUserSerializer(
        source='user_id',
        read_only=True
    )
    cooking_time = serializers.IntegerField(
        validators=(
            MinValueValidator(
                1,
                message='Время приготовления >= 1'
            ),  # Проверка данных времени приготовления
        ),
    )

    class Meta:
        fields = (
            'ingredients',
            'tags',
            'author',
            'image',
            'name',
            'text',
            'cooking_time',
        )
        model = Recipes

    def validate_ingredients(self, value):
        """ Проверка, не повторяются ли ингридиенты в рецепте """
        ingredients = self.initial_data.get('ingredients')
        ingredients = [item['id'] for item in ingredients]
        for ingredient in ingredients:
            if ingredients.count(ingredient) > 1:
                raise exceptions.ValidationError(
                    {'ingredients': 'Добавлены два одинаковых ингридиента'}
                )
        return value

    def create(self, validated_data):
        """ Создание нового рецепта """
        tags = validated_data.pop('tags')
        ingredients_data = validated_data.pop('recipes_list')
        recipe = Recipes.objects.create(**validated_data)
        recipe.tags.set(tags)
        for ingredient in ingredients_data:
            Ingredients_list.objects.create(
                recipes_id=recipe,
                ingr_id=ingredient.get('ingr_id'),
                quantity=ingredient.get('quantity')
            ).save()
        return recipe

    def update(self, instance, validated_data):
        """ Изменение данных рецепта """
        tags = validated_data.pop('tags')
        ingredients_data = validated_data.pop('recipes_list')
        instance.ingredients_lists.clear()
        instance.tags.set(tags)
        for ingredient in ingredients_data:
            Ingredients_list.objects.update_or_create(
                recipes_id=instance,
                ingr_id=ingredient.get('ingr_id'),
                quantity=ingredient.get('quantity')
            )
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        """ Обрабатываем все записи и выводим """
        recipe = super().to_representation(instance)
        recipe = RecipesSerializerList(
            instance,
            context={'request': self.context.get('request')}
        ).data
        return recipe


class FavoriteRecipesSerializer(serializers.ModelSerializer):
    """ Сериализатор избранных рецептов """
    name = serializers.ReadOnlyField(
        source='recipes_id.recipe_name',
        read_only=True)
    image = serializers.ImageField(
        source='recipes_id.image',
        read_only=True)
    coocking_time = serializers.IntegerField(
        source='recipes_id.cooking_time',
        read_only=True)
    id = serializers.PrimaryKeyRelatedField(
        source='recipes_id',
        read_only=True)

    class Meta:
        model = Favorite_recipes
        fields = ('id', 'name', 'image', 'coocking_time')


class RecipesSerializerShortList(serializers.ModelSerializer):
    """ Сериализатор для отображения неполных данных рецепта """
    name = serializers.CharField(source='recipe_name')

    class Meta:
        model = Recipes
        fields = ('id', 'name', 'image', 'cooking_time',)


class FollowRecipesSerializer(serializers.ModelSerializer):
    """ Сериализатор подписок на автора """
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        """ Добавлен ли рецепт в список покупок True/False """
        user = self.context.get('request').user
        if not user.is_anonymous:
            return Follow.objects.filter(
                user_id=user,
                author=obj.author).exists()
        return False

    def get_recipes_count(self, obj):
        """ Счетчик рецептов автора """
        return Recipes.objects.filter(user_id=obj.author).count()

    def get_recipes(self, obj):
        """ Используем сериализатор сокращеных данных рецепта """
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = Recipes.objects.filter(user_id=obj.author)
        # Значение должнобыть числовым и >0
        if limit and limit.isdigit():
            recipes = recipes[:int(limit)]
        return RecipesSerializerShortList(recipes, many=True).data


class ShopingListSerializer(serializers.ModelSerializer):
    """ Сериализатор списка покупок """
    id = serializers.PrimaryKeyRelatedField(
        source='recipes_id',
        read_only=True)
    name = serializers.ReadOnlyField(
        source='recipes_id.recipe_name',
        read_only=True
    )
    image = serializers.ImageField(
        source='recipes_id.image',
        read_only=True
    )
    cooking_time = serializers.IntegerField(
        source='recipes_id.cooking_time',
        read_only=True)

    class Meta:
        model = Shoping_list
        fields = ('id', 'name', 'image', 'cooking_time')
