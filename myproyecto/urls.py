from django.urls import path, include
from django.conf import settings
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from blog.views import AnimalViewSet,LevelViewSet, UserProgressViewSet, CustomAnimalImageViewSet
router = DefaultRouter()
router.register(r'animals', AnimalViewSet)
router.register(r'levels', LevelViewSet)
router.register(r'progress', UserProgressViewSet, basename='progress')
router.register(r'custom-animals', CustomAnimalImageViewSet, basename='custom-animals')

urlpatterns = [
    path('', include(router.urls)),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)