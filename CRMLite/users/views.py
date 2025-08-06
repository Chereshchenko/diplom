from rest_framework import permissions, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView

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

class CurrentUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        serializer = RegisterSerializer(request.user)
        return Response(serializer.data)  
