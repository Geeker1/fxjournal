from rest_framework import serializers
from .models import TimeStamp, ForexEntry, BinaryEntry


class StampSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeStamp
        fields = '__all__'
        # depth = 1


class BinarySerializer(serializers.ModelSerializer):
    class Meta:
        model = BinaryEntry
        fields = '__all__'


class ForexSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForexEntry
        fields = '__all__'
