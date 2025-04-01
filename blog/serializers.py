from rest_framework import serializers
from .models import Mensajes

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mensajes
        fields = ["id", "titulo", "contenido"]
    
    