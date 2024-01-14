"""
URL configuration for meta project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import (
    SpectacularAPIView, 
    SpectacularJSONAPIView, 
    SpectacularRedocView, 
    SpectacularSwaggerView
)
from files.api.viewsets import FileViewset
from microsoft.api.viewsets import MicrosoftViewSet
from user.api.viewsets import UserViewset


router = routers.DefaultRouter()
router.register(
    r'users', 
    UserViewset, 
    basename='User'
)
router.register(
    r'file', 
    FileViewset, 
    basename='File'
)
router.register(
    r'microsoft', 
    MicrosoftViewSet, 
    basename='Microsoft'
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('auth/login/', obtain_auth_token),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/swagger/", SpectacularSwaggerView.as_view(url_name="schema")),
    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
