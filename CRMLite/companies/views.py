from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from companies.models import Company, Storage
from companies.serializers import *
from users.models import User
from users.permissions import IsCompanyOwner, IsCompanyEmployee
        
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsCompanyOwner()]
        return [permissions.IsAuthenticated()]
    
    def perform_create(self, serializer):
        if self.request.user.company:
            raise serializers.ValidationError("Вы уже привязаны к компании")
        company = serializer.save(owner=self.request.user)
        self.request.user.is_company_owner = True
        self.request.user.company = company
        self.request.user.save()

class StorageViewSet(viewsets.ModelViewSet):
    serializer_class = StorageSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.company:
            return Storage.objects.filter(company=user.company)
        return Storage.objects.none()
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsCompanyOwner()]
        return [IsCompanyEmployee()]
    
    def perform_create(self, serializer):
        if not self.request.user.is_company_owner:
            raise permissions.exceptions.PermissionDenied("Только владелец компании может создавать склады")
        serializer.save(company=self.request.user.company)

class AttachUserSerializer(serializers.Serializer):
    email = serializers.EmailField()

class CompanyUserViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsCompanyOwner]
    
    def get_serializer_class(self):
        return AttachUserSerializer
    
    @action(detail=False, methods=['post'])
    def attach_user(self, request):
        serializer = AttachUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            user = User.objects.get(email=serializer.validated_data['email'])
        except User.DoesNotExist:
            return Response(
                {"error": "Пользователь с таким email не найден"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if user.company:
            return Response(
                {"error": "Пользователь уже привязан к другой компании"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not request.user.is_company_owner:
            return Response(
                {"error": "Только владелец компании может прикреплять пользователей"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        user.company = request.user.company
        user.save()
        
        return Response(
            {"status": "Пользователь успешно привязан к компании"},
            status=status.HTTP_200_OK
        )
               