from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Mensajes
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Mensajes.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]
# Create your views here.
