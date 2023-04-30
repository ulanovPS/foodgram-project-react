from djoser.serializers import UserSerializer
from rest_framework import serializers

from grocery_assistant.models import Ingredients, Tags, Follow
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
        
