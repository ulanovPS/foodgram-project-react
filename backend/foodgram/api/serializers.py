from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField 
from rest_framework import serializers

from grocery_assistant.models import (Favorite_recipes, Follow, Ingredients,
                                      Ingredients_list, Recipes, Shoping_list,
                                      Tags)
from users.models import User


class TagsSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='tag_name')

    class Meta:
        fields = ('id', 'name', 'color', 'slug')
        model = Tags


class IngredientsSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='ingr_name')

    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredients


class CustomUserSerializer(UserSerializer):
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
        user = self.context.get('request').user
        if not user.is_anonymous:
            return Follow.objects.filter(user_id=user, author=obj).exists()
        return False

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class TagsSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField(
        read_only=True,
        source='tag_name'
    )

    class Meta:
        fields = (
            'id',
            'name',
            'color',
            'slug'
        )
        model = Tags


class Ingredients_listSerializer(serializers.ModelSerializer):
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
    author = UserSerializer(source='user_id')
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
        user = self.context.get('request').user
        if not user.is_anonymous:
            return Shoping_list.objects.filter(recipes_id=obj).exists()
        return False

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if not user.is_anonymous:
            return Favorite_recipes.objects.filter(recipes_id=obj).exists()
        return False


class AddIngredientsSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredients.objects.all(),
        source='ingr_id.id'
    )
    amount = serializers.IntegerField(source='quantity')
    class Meta:
        model = Ingredients_list
        fields = ('id', 'amount')

class RecipesSerializerAdd(serializers.ModelSerializer):
    ingredients = AddIngredientsSerializer(
        many=True,
        read_only=True
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tags.objects.all(),
        many=True,
    )
    image = Base64ImageField()
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
        source='user_id'
    )
    text = serializers.ReadOnlyField(
        source='description',
    )
    name = serializers.ReadOnlyField(
        source='recipe_name'
    )

    class Meta:
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
            'author'
        )
        model = Recipes
"""
    def create(self, validated_data):
            
        achievements = validated_data.pop('ingredients')
        rec = Recipes.objects.create(**validated_data)
        for achievement in achievements:
            val_ingr_id, status = Ingredients.objects.get_or_create(**achievement)
            Ingredients_list.objects.create(ingr_id=val_ingr_id, recipes_id=rec)
        return rec 
"""