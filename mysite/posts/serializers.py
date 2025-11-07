from rest_framework import serializers
from django.utils import timezone
from .models import Post, Category, Topic


class PostSimpleSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=150)
    text = serializers.CharField()
    slug = serializers.SlugField()
    topic_id = serializers.IntegerField()
    created_by_id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def validate_title(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("Nazwa może zawierać tylko litery.")
        return value

    def validate_created_at(self, value):
        if value and value > timezone.now():
            raise serializers.ValidationError("Data dodania nie może być z przyszłości.")
        return value

    def create(self, validated_data):
        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('text', instance.text)
        instance.slug = validated_data.get('slug', instance.slug)
        if 'topic_id' in validated_data:
            instance.topic_id = validated_data['topic_id']
        if 'created_at' in validated_data:
            instance.created_at = validated_data['created_at']
        instance.save()
        return instance


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class TopicSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
    )

    class Meta:
        model = Topic
        fields = ['id', 'name', 'category', 'category_id', 'created']
        read_only_fields = ['created']
