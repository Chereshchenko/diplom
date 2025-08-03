from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Company, Storage, User
from .serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView
from .permissions import IsCompanyOwner, IsCompanyEmployee

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                "message": "Пользователь успешно зарегистрирован",
                "user": serializer.data
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )
        
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

class CurrentUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        serializer = RegisterSerializer(request.user)
        return Response(serializer.data)
