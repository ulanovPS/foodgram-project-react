from rest_framework import serializers

from grocery_assistant.models import Unit_of_measure


class Unit_of_measure_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Unit_of_measure
        fields = ('unit_name',)
