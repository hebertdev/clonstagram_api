# core/urls.py
from django.urls import path, include

#djangorf

from rest_framework.routers import DefaultRouter

from .views import users as user_views


router = DefaultRouter()
router.register(r'users', user_views.UserViewSet , basename="users")

urlpatterns = [
	path('' , include(router.urls))
	
]
