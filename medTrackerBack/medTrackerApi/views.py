from django.shortcuts import render
# Create your views here.
from rest_framework import viewsets
from datetime import *
from django.utils import timezone
from django.forms import ValidationError
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.decorators import action
from django.contrib.auth.hashers import check_password
from rest_framework import viewsets, status
from .models import CustomUser, DatosDeSalud, Notificaciones, Registrar
from .serializers import (CustomUserSerializer, DatosDeSaludSerializer,NotificacionesSerializer, RegistrarSerializer, LoginSerializer)
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

# Vista del conjunto para el Usuario Personalizado
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    @action (methods=["GET"], detail=False, serializer_class=LoginSerializer, permission_classes=[IsAuthenticated])
    def current_user(self, request):
        return Response({
            "user": str(request.user),
            "id" : str(request.user.pk),
            "auth": str(request.auth), 
            "is_superuser":(request.user.is_superuser)
        }, status=status.HTTP_200_OK) 

    @action (methods=["POST"], detail=False, serializer_class=LoginSerializer, permission_classes=[AllowAny])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            telefono = serializer.validated_data["telefono"]
            password = serializer.validated_data["password"]

            try:
                user = CustomUser.objects.get(telefono=telefono) #select * from user where email=?, email
            except BaseException as e:
                raise ValidationError({"error": str(e)})

            if not check_password(password, user.password):
                raise ValidationError({"error": "Incorrect Password"})
            
            user.last_login = timezone.now() 
            user.save()
            print(user)
            token, created = Token.objects.get_or_create(user=user) # que hago con esto??
            print(token)

            return Response({"token":token.key}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def create(self, request):
        serializer = CustomUserSerializer(data=request.data)
        user = None
        if serializer.is_valid():
            user = CustomUser.objects.create_user(
                telefono = serializer.validated_data["telefono"], 
                password = serializer.validated_data["password"], 
                nombre = serializer.validated_data["nombre"], 
                apellidos = serializer.validated_data["apellidos"], 
                esPaciente = serializer.validated_data["esPaciente"], 
                estatura = serializer.validated_data["estatura"], 
                sexo = serializer.validated_data["sexo"], 
                antecedentes = serializer.validated_data["antecedentes"],
                is_active = serializer.validated_data["is_active"],  
                #last_login = serializer.validated_data["last_login"],
                is_superuser = serializer.validated_data["is_superuser"]
            )
            user.last_login = timezone.now()  # Instead of validating data, set the last login manually to right now since it wont get posted
            user.save()
            response = CustomUserSerializer(instance=user, context={'request': request} )

            return Response(response.data, status=status.HTTP_200_OK)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        

# Vista del conjunto para Datos de Salud
class DatosDeSaludViewSet(viewsets.ModelViewSet):
    queryset = DatosDeSalud.objects.all()
    serializer_class = DatosDeSaludSerializer
    permission_classes = [AllowAny]
    authentication_classes = (SessionAuthentication, TokenAuthentication)

# Vista del conjunto para Notificaciones
class NotificacionesViewSet(viewsets.ModelViewSet):
    queryset = Notificaciones.objects.all()
    serializer_class = NotificacionesSerializer
    permission_classes = [AllowAny]
    authentication_classes = (SessionAuthentication, TokenAuthentication)

# Vista del conjunto para Registrar
class RegistrarViewSet(viewsets.ModelViewSet):
    queryset = Registrar.objects.all()
    serializer_class = RegistrarSerializer
    permission_classes = [AllowAny]
    authentication_classes = (SessionAuthentication, TokenAuthentication)
