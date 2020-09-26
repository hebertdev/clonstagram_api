# core/urls.py
from django.urls import path, include

#djangorf

from rest_framework.routers import DefaultRouter

# view

from .views import posts as post_views
from .views import comments as coment_views
from .views import likes as likes_views

router = DefaultRouter()
router.register(r'posts',post_views.PostViewSet , basename="post")
router.register(r'posts/(?P<slug_name>[a-zA-Z0-9_-]+)/comentarios',
    coment_views.CommentViewSet,
    basename='comments'
)
router.register(r'posts/(?P<slug_name>[a-zA-Z0-9_-]+)/likes',
    likes_views.LikeViewSet,
    basename='likepost'
)

urlpatterns = [
	path('' , include(router.urls))
]