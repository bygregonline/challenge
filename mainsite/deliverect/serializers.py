from rest_framework import serializers
from .models import (Menu,
                    Order,
                    OrderItem)

class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ('description','uuid', 'price', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('created_at','uuid', 'amount', 'note')


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('menu', 'quantity')