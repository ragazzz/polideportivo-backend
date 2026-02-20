from django.contrib import admin
from django.urls import path, include
from core.auth_views import login_view, logout_view, check_auth

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('api/auth/login/', login_view, name='login'),
    path('api/auth/logout/', logout_view, name='logout'),
    path('api/auth/me/', check_auth, name='check_auth'),
]
