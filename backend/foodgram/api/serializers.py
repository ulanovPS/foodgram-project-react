from rest_framework import serializers

from grocery_assistant.models import Ingredients, Tags
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


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )
        model = User

    def get_is_subscribed(self, obj):

        return 'test'
