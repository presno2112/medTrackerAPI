from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('medTrackerApi.urls')),  # Incluir URLs de la aplicación
    path('api-auth/', include('rest_framework.urls')),  # Para autenticación de DRF
]
