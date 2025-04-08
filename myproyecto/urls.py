from django.urls import path, include
from rest_framework.routers import DefaultRouter
from blog.views import AnimalViewSet,LevelViewSet, UserProgressViewSet, CustomAnimalImageViewSet
router = DefaultRouter()
router.register(r'animals', AnimalViewSet)
router.register(r'levels', LevelViewSet)
router.register(r'progress', UserProgressViewSet, basename='progress')
router.register(r'custom-animals', CustomAnimalImageViewSet, basename='custom-animals')

urlpatterns = [
    path('', include(router.urls)),
]