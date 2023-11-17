from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, telefono, password=None, **extra_fields):
        if not telefono:
            raise ValueError('El número de teléfono es obligatorio.')
        user = self.model(telefono=telefono, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, telefono, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')

        return self.create_user(telefono, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    telefono = models.BigIntegerField(unique=True, primary_key=True)
    nombre = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    esPaciente = models.BooleanField(default=False)
    estatura = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    sexo = models.CharField(max_length=1, null=True, blank=True)
    antecedentes = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = 'telefono'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.nombre} {self.apellidos} - {self.telefono}"

# Modelo de Datos de Salud
class DatosDeSalud(models.Model):
    idSituacion = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='datos_salud')
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    unidadesMedicion = models.CharField(max_length=255, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

# Modelo de Notificaciones
class Notificaciones(models.Model):
    idSituacion = models.ForeignKey(DatosDeSalud, on_delete=models.CASCADE, related_name='notificaciones')
    unidad = models.CharField(max_length=255)
    cantidad = models.IntegerField()
    fechaInicio = models.DateField()
    fechaFin = models.DateField()

    def __str__(self):
        return f"Notificación para {self.idSituacion.nombre}"

# Modelo de Registro
class Registrar(models.Model):
    idSituacion = models.ForeignKey(DatosDeSalud, related_name='registros', on_delete=models.CASCADE)
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='registros')
    fecha_hora = models.DateTimeField()
    cantidad = models.IntegerField()
    notas = models.TextField()

    def __str__(self):
        return f"Registro en {self.fecha_hora} para {self.idSituacion.nombre}"
