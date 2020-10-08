from django.contrib import admin
from django.urls import path , include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , include(('apps.users.urls', 'users') , namespace="users")),
    path('' , include(('apps.posts.urls', 'posts') , namespace="posts")),
    
   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

