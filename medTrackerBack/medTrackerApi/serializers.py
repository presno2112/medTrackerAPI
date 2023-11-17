from rest_framework import serializers
from .models import CustomUser, DatosDeSalud, Notificaciones, Registrar

# Serializador de Usuario Personalizado
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"
        extra_kwargs = {
            "password": {
            "write_only": True,
            "style":{"input_type":"password"}, 

            },
            "last_login": {
            "read_only" : True    
            }
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

# Serializador de Datos de Salud
class DatosDeSaludSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatosDeSalud
        fields = '__all__'

# Serializador de Notificaciones
class NotificacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificaciones
        fields = '__all__'

# Serializador de Registro
class RegistrarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registrar
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    password = serializers.CharField(
        required=True,
        style={'input_type': 'password'}
    )
    phone = serializers.CharField(
        required=True
    )
