from rest_framework import serializers
from .models import TimeStamp, ForexEntry, BinaryEntry, Reason, Lesson


class StampSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeStamp
        fields = '__all__'
        # depth = 1


class ReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reason
        fields = ('image', 'text',)


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('image', 'text',)


class BaseSerializer(serializers.ModelSerializer):
    r_text = serializers.CharField(write_only=True)
    l_text = serializers.CharField(write_only=True)
    r_image = serializers.ImageField(write_only=True)
    l_image = serializers.ImageField(write_only=True)
    reason = ReasonSerializer(read_only=True)
    lesson = LessonSerializer(read_only=True)

    def create(self, validated_data):
        entry = self.Meta.model.objects.create_entry(
            **validated_data)
        return entry


class BinarySerializer(BaseSerializer):

    class Meta:
        model = BinaryEntry
        fields = '__all__'


class ForexSerializer(BaseSerializer):
    # reason = ReasonSerializer()
    # lesson = LessonSerializer()

    class Meta:
        model = ForexEntry
        fields = '__all__'
