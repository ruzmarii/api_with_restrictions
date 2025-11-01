from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

from .models import Advertisement
from .serializers import AdvertisementSerializer
from .filters import AdvertisementFilter
from .permissions import IsOwnerOrReadOnly, IsOwner

class AdvertisementViewSet(viewsets.ModelViewSet):
    """ViewSet для объявлений"""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get_permissions(self):
        """Получение прав для действий"""
        if self.action in ["create"]:
            return [IsAuthenticated()]
        elif self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        else:
            return [AllowAny()]

    def get_queryset(self):
        """Получение queryset с учетом прав доступа"""
        queryset = super().get_queryset()
        
        # Для неавторизованных пользователей и для списковых запросов
        # показываем все объявления (фильтрация по статусу будет через filters)
        if self.action == "list":
            return queryset
            
        return queryset

    def destroy(self, request, *args, **kwargs):
        """Удаление объявления с проверкой прав"""
        instance = self.get_object()
        
        # Проверяем, что пользователь является создателем объявления
        if instance.creator != request.user:
            return Response(
                {"detail": "У вас нет прав для удаления этого объявления"},
                status=status.HTTP_403_FORBIDDEN
            )
            
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)