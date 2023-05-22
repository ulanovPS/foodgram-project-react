from django.core import exceptions
from django.core.validators import MinValueValidator
from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField
from grocery_assistant.models import (FavoriteRecipe, Follow, Ingredient,
                                      IngredientRecipe, Recipe, ShopingList,
                                      Tag)
from rest_framework import serializers
from users.models import User


class TagsSerializer(serializers.ModelSerializer):
    """ Сериализатор тегов """

    class Meta:
        fields = ('id', 'name', 'color', 'slug')
        model = Tag


class IngredientsSerializer(serializers.ModelSerializer):
    """ Сериализатор ингридиентов """

    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredient


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
            return Follow.objects.filter(user=user, author=obj).exists()
        return False

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """ Вложеные сериализатор отображения рецептов """
    id = serializers.ReadOnlyField(
        source='ingredient.id'
    )
    name = serializers.ReadOnlyField(
        source='ingredient.name'
    )
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipesSerializerList(serializers.ModelSerializer):
    """ Сериализатор отображения рецептов """
    text = serializers.StringRelatedField(
        read_only=True,
        source='description'
    )
    name = serializers.StringRelatedField(
        read_only=True,
    )
    tags = TagsSerializer(read_only=True, many=True)
    author = CustomUserSerializer()
    is_in_shopping_cart = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    ingredients = IngredientRecipeSerializer(
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
        model = Recipe

    def get_is_in_shopping_cart(self, obj):
        """ Добавлен ли рецепт в список покупок True/False """
        user = self.context.get('request').user
        if not user.is_anonymous:
            return ShopingList.objects.filter(
                recipes=obj,
                user=user.id
            ).exists()
        return False

    def get_is_favorited(self, obj):
        """ Добавлен ли рецепт в избранное True/False """
        user = self.context.get('request').user
        if not user.is_anonymous:
            return FavoriteRecipe.objects.filter(
                recipes=obj,
                user=user.id
            ).exists()
        return False


class AddIngredientsSerializer(serializers.ModelSerializer):
    """ Вложеный сериализатор добавления нового рецепта """
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient'
    )
    amount = serializers.IntegerField(
        validators=(
            MinValueValidator(
                1,
                message='Минимальное значение >= 1'
            ),  # Проверка для значения кол-ва ингридиента
        ),
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')


class RecipesSerializerAdd(serializers.ModelSerializer):
    """ Сериализатор добавления рецепта """
    ingredients = AddIngredientsSerializer(
        many=True,
        source='recipes_list'
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    image = Base64ImageField()
    text = serializers.CharField(
        source='description',
    )
    author = CustomUserSerializer(
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
        model = Recipe

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

    def bulk(self, ingredients, recipes):
        IngredientRecipe.objects.bulk_create(
            [IngredientRecipe(
                recipes=recipes,
                ingredient=ingredient.get('ingredient'),
                amount=ingredient['amount']
            )for ingredient in ingredients]
        )

    def create(self, validated_data):
        """ Создание нового рецепта """
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('recipes_list')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.bulk(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        """ Изменение данных рецепта """
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('recipes_list')
        instance.tags.clear()
        instance.tags.set(tags)
        instance.ingredients.clear()
        self.bulk(ingredients, instance)
        instance.save()
        return instance

    def to_representation(self, instance):
        """ Обрабатываем все записи и выводим """
        return RecipesSerializerList(
            instance,
            context={'request': self.context.get('request')}
        ).data


class FavoriteRecipesSerializer(serializers.ModelSerializer):
    """ Сериализатор избранных рецептов """
    name = serializers.ReadOnlyField(
        source='recipes.name',
        read_only=True)
    image = serializers.ImageField(
        source='recipes.image',
        read_only=True)
    coocking_time = serializers.IntegerField(
        source='recipes.cooking_time',
        read_only=True)
    id = serializers.PrimaryKeyRelatedField(
        source='recipes',
        read_only=True)

    class Meta:
        model = FavoriteRecipe
        fields = ('id', 'name', 'image', 'coocking_time')


class RecipesSerializerShortList(serializers.ModelSerializer):
    """ Сериализатор для отображения неполных данных рецепта """

    class Meta:
        model = Recipe
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
                user=user,
                author=obj.author).exists()
        return False

    def get_recipes_count(self, obj):
        """ Счетчик рецептов автора """
        return Recipe.objects.filter(author=obj.author).count()

    def get_recipes(self, obj):
        """ Используем сериализатор сокращеных данных рецепта """
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = Recipe.objects.filter(author=obj.author)
        # Значение должнобыть числовым и >0
        if limit and limit.isdigit():
            recipes = recipes[:int(limit)]
        return RecipesSerializerShortList(recipes, many=True).data


class ShopingListSerializer(serializers.ModelSerializer):
    """ Сериализатор списка покупок """
    id = serializers.PrimaryKeyRelatedField(
        source='recipes',
        read_only=True)
    name = serializers.ReadOnlyField(
        source='recipes.name',
        read_only=True
    )
    image = serializers.ImageField(
        source='recipes.image',
        read_only=True
    )
    cooking_time = serializers.IntegerField(
        source='recipes.cooking_time',
        read_only=True)

    class Meta:
        model = ShopingList
        fields = ('id', 'name', 'image', 'cooking_time')
