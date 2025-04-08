from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Count, Avg
from django.contrib.auth.models import AnonymousUser

from .models import Animal, Level, UserProgress, CustomAnimalImage
from .serializers import (
    AnimalSerializer, 
    LevelSerializer, 
    UserProgressSerializer,
    CustomAnimalImageSerializer
)

class AnimalViewSet(viewsets.ModelViewSet):  
    """
    API endpoint that allows animals to be viewed and created.
    """
    queryset = Animal.objects.filter(is_active=True)
    serializer_class = AnimalSerializer

    @action(detail=False)
    def by_vowel(self, request):
        """Get animals grouped by starting vowel"""
        vowels = ['a', 'e', 'i', 'o', 'u']
        result = {}
        
        for vowel in vowels:
            animals = self.queryset.filter(starting_vowel=vowel)
            result[vowel] = AnimalSerializer(animals, many=True, context={'request': request}).data
            
        return Response(result)

class LevelViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows game levels to be viewed.
    """
    queryset = Level.objects.filter(is_active=True)
    serializer_class = LevelSerializer  
    
    @action(detail=True)
    def start(self, request, pk=None):
        """Start or resume a level"""
        level = self.get_object()
        user = request.user if request.user.is_authenticated else None
        
        if not user:
            return Response({"error": "Authentication required to track progress."}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Get or create progress record
        progress, created = UserProgress.objects.get_or_create(
            user=user,
            level=level
        )
        
        serializer = UserProgressSerializer(progress)
        return Response(serializer.data)

class UserProgressViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to track their progress.
    """
    serializer_class = UserProgressSerializer
    
    def get_queryset(self):
        """Return only the current user's progress"""
        user = self.request.user
        if user.is_authenticated:
            return UserProgress.objects.filter(user=user)
        return UserProgress.objects.none()
    
    @action(detail=False)
    def summary(self, request):
        """Get a summary of user's progress across all levels"""
        user = request.user
        
        if not user.is_authenticated:
            return Response({
                "error": "Authentication required for progress summary."
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        total_levels = Level.objects.filter(is_active=True).count()
        completed_levels = UserProgress.objects.filter(
            user=user,
            completed=True
        ).count()
        
        avg_score = UserProgress.objects.filter(
            user=user
        ).aggregate(avg_score=Avg('score'))
        
        return Response({
            'total_levels': total_levels,
            'completed_levels': completed_levels,
            'completion_percentage': (completed_levels / total_levels * 100) if total_levels > 0 else 0,
            'average_score': avg_score['avg_score'] or 0
        })
    
    @action(detail=True, methods=['post'])
    def update_score(self, request, pk=None):
        """Update the score for a level"""
        progress = self.get_object()
        score = request.data.get('score', 0)
        completed = request.data.get('completed', False)
        
        progress.score = max(progress.score, int(score))  # Only update if better than previous
        progress.completed = progress.completed or completed  # Once completed, stays completed
        progress.save()
        
        serializer = self.get_serializer(progress)
        return Response(serializer.data)

class CustomAnimalImageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to manage their custom animal images.
    """
    serializer_class = CustomAnimalImageSerializer
    
    def get_queryset(self):
        """Return only the current user's custom animal images"""
        user = self.request.user
        if user.is_authenticated:
            return CustomAnimalImage.objects.filter(user=user)
        return CustomAnimalImage.objects.none()
    
    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_authenticated:
            raise PermissionDenied("Authentication required to create custom animal images.")
        serializer.save(user=user)