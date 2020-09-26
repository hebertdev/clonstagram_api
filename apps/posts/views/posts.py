"""posts vies"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins , status , viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action






#permisions

from apps.posts.permissions.posts import IsPostOwner

from apps.posts.serializers import PostModelSerializer , CommentsPostModelSerializer , CreateLikeSerializer
from apps.posts.models import (Post , Comment)





	
	
	




class PostViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
	queryset = Post.objects.all().order_by('-created')
	serializer_class = PostModelSerializer
	lookup_field = 'id'

	
	def get_permissions(self):
		permissions = [IsAuthenticated]
		if self.action in ['update' , 'partial_update' , 'destroy']:
			permissions.append(IsPostOwner)
		return [p() for p in permissions]

	def perform_create(self , serializer):
		"""assign user at post"""
		user = self.request.user
		profile = user.profile
		post = serializer.save(user=user , profile=profile)


	def get_serializer_class(self):
		if self.action == 'likes':
			return CreateLikeSerializer
		return PostModelSerializer

	@action(detail=True , methods=['post'])
	def likes(self , request , *args , **kwargs):
		post = self.get_object()
		serializer_class = self.get_serializer_class()
		serializer = serializer_class(
			post,
			data={'user':request.user.pk},
			context={'post':
			post , 'user':request.user.pk},
		)

		serializer.is_valid(raise_exception=True)
		post = serializer.save()
		data = PostModelSerializer(post).data
		return Response(data , status=status.HTTP_200_OK)

	

	def retrieve(self , request , *args , **kwargs):
		response = super(PostViewSet , self).retrieve(request, *args , *kwargs)
		id_post = response.data.get('id')
		comments = Comment.objects.filter(post=id_post)
		data = {
			'post':response.data,
			'comments':CommentsPostModelSerializer(comments , many=True).data
		}

		response.data = data
		return response




