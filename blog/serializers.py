from rest_framework import serializers
from .models import Animal, Level, UserProgress, CustomAnimalImage

class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = ['name', 'starting_vowel', 'image']  # Excluye 'id'

class LevelSerializer(serializers.ModelSerializer):
    # Usamos PrimaryKeyRelatedField para POST (IDs) y AnimalSerializer para GET (detalles)
    animals = AnimalSerializer(many=True, read_only=True)  # Solo lectura (detalles en la respuesta)
    animal_ids = serializers.PrimaryKeyRelatedField(queryset=Animal.objects.all(), many=True, write_only=True)  # Solo escritura (IDs en la solicitud)

    class Meta:
        model = Level
        fields = ['id', 'name', 'description', 'difficulty', 'animals', 'animal_ids']
    
    def create(self, validated_data):
        animal_ids = validated_data.pop('animal_ids', [])
        level = Level.objects.create(**validated_data)
        level.animals.set(animal_ids)  # Relacionamos los IDs con el nivel
        return level
    
    def update(self, instance, validated_data):
        animal_ids = validated_data.pop('animal_ids', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        instance.animals.set(animal_ids)  # Actualizamos las relaciones con los animales
        return instance
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