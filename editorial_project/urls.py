"""
URL configuration for editorial_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# En editorial_project/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # --- LÍNEA CORREGIDA Y FINAL ---
    # Aquí le decimos a Django:
    # 1. Incluye todas las URLs del archivo 'produccion.urls'.
    # 2. Y muy importante: agrúpalas todas bajo el "apellido" o namespace 'produccion'.
    path('produccion/', include('produccion.urls', namespace='produccion')),
    path('consignaciones/', include('produccion.urls_consignacion')),
]