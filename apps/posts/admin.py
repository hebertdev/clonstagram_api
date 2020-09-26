"""Post models admin."""

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Models
from apps.posts.models import Post , Comment



@admin.register(Post)
class ProfileAdmin(admin.ModelAdmin):
    """Profile model admin."""

    list_display = ('user', 'title')
  

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Profile model admin."""

    list_display = ('id', 'user')
  
