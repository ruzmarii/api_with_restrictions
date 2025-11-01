from rest_framework import serializers
from .models import Advertisement, AdvertisementStatusChoices
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя"""
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

class AdvertisementSerializer(serializers.ModelSerializer):
    """Сериализатор для объявления"""
    creator = UserSerializer(read_only=True)
    
    class Meta:
        model = Advertisement
        fields = ['id', 'title', 'description', 'status', 'creator', 'created_at', 'updated_at']
        read_only_fields = ['creator', 'created_at', 'updated_at']

    def validate_status(self, value):
        """Валидация статуса"""
        if value not in AdvertisementStatusChoices.values:
            raise serializers.ValidationError("Недопустимый статус")
        return value

    def create(self, validated_data):
        """Создание объявления с автоматическим назначением создателя"""
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)