from rest_framework import serializers
from .models import Menu

class ModelSerializer(serializers.ModelSerializer):



    class Meta:
        model = Menu
        fields = ('description','uuid', 'price', 'quantity')