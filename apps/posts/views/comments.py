"""Rides views."""

# Django REST Framework
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import IsAuthenticated

#permisions

from apps.posts.permissions.posts import IsPostOwner

from apps.posts.serializers import PostModelSerializer , CommentsPostModelSerializer , CreateCommentSerializer
from apps.posts.models import (Post , Comment)


class CommentViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
	serializer_class = CreateCommentSerializer


	def  dispatch(self , request , *args , **kwargs):
		self.slug_name = kwargs['slug_name']
		print(self.slug_name)
		return super(CommentViewSet,self).dispatch(request,*args,**kwargs)


	
	def get_permissions(self):
		permissions = [IsAuthenticated]
		if self.action in ['update' , 'partial_update' , 'destroy']:
			permissions.append(IsPostOwner)
		return [p() for p in permissions]


	def get_serializer_context(self):
		value = self.slug_name
		self.post = get_object_or_404(Post, id=value)
		context = super(CommentViewSet , self).get_serializer_context()
		context['post'] = self.post
		context['user'] = self.request.user
		context['profile'] = self.request.user.profile
		return context




	



