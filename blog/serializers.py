from rest_framework import serializers
from .models import Animal, Level, UserProgress, CustomAnimalImage

class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = ['id', 'name', 'starting_vowel', 'image']

class LevelSerializer(serializers.ModelSerializer):
    animals = AnimalSerializer(many=True, read_only=True)
    
    class Meta:
        model = Level
        fields = ['id', 'name', 'description', 'difficulty', 'animals']

class UserProgressSerializer(serializers.ModelSerializer):
    level_name = serializers.CharField(source='level.name', read_only=True)
    
    class Meta:
        model = UserProgress
        fields = ['id', 'level', 'level_name', 'score', 'completed', 'last_played']
        read_only_fields = ['user', 'last_played']
    
    def create(self, validated_data):
        # Ensure the user from the request is used
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class CustomAnimalImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomAnimalImage
        fields = ['id', 'name', 'starting_vowel', 'image', 'created_at']
        read_only_fields = ['user', 'created_at']
    
    def create(self, validated_data):
        # Ensure the user from the request is used
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)