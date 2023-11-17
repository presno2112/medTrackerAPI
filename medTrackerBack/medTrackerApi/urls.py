from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet, DatosDeSaludViewSet, NotificacionesViewSet, RegistrarViewSet

router = DefaultRouter()
router.register(r'usuarios', CustomUserViewSet)
router.register(r'datosdesalud', DatosDeSaludViewSet)
router.register(r'notificaciones', NotificacionesViewSet)
router.register(r'registros', RegistrarViewSet)

urlpatterns = [
    path('', include(router.urls))
]
