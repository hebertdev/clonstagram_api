#django

import json

#restaframework
from rest_framework import mixins , status , viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView

from rest_framework.response import Response

#serializer
from apps.users.serializers.users import (UserLoginSerializer , UserModelSerializer  , UserSignUpSerializer , FollowSerializer)
from apps.users.serializers.profiles import ProfileModelSerializer 

from apps.users.models import User
from apps.posts.models import Post

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)

from apps.users.permissions import IsAccountOwner





from apps.posts.serializers import PostModelSerializer


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet,
                  mixins.ListModelMixin):

	queryset = User.objects.all()
	serializer_class = UserModelSerializer
	lookup_field = 'username'

	def get_permissions(self):
		if self.action in ['signup', 'login']:
			permissions = [AllowAny]
		elif self.action in ['retrieve']:
			permissions = [IsAuthenticated]
		elif self.action in ['update', 'partial_update', 'profile']:
			permissions = [IsAuthenticated , IsAccountOwner]
		elif self.action in ['follow']:
			permissions = [IsAuthenticated , AllowAny]
		else:
			permissions = [IsAuthenticated]

		return [p() for p in permissions]

	def get_serializer_class(self):
		if self.action == 'follow':
			return FollowSerializer
		return UserModelSerializer

	@action(detail=True , methods=['put' , 'patch'])
	def profile(self , request , *args , **kwargs):
		user = self.get_object()
		profile = user.profile
		partial = request.method == 'PATCH'
		serializer = ProfileModelSerializer(
			profile,
			data=request.data,
			partial=partial
		)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		data = UserModelSerializer(user).data
		return Response(data)

	@action(detail=True , methods=['post'])
	def follow(self , request , *args , **kwargs):
		user_to_follow = self.get_object()
		serializer_class = self.get_serializer_class()
		serializer = serializer_class(
			user_to_follow,
			data={'user':request.user.pk},
			context={'user_to_follow':user_to_follow , 'user':request.user},
			partial=True
		) 

		serializer.is_valid(raise_exception=True)
		user_to_follow = serializer.save()
		data = UserModelSerializer(user_to_follow).data
		return Response(data , status=status.HTTP_200_OK)
	

	@action(detail=False , methods=['post'])
	def login(self, request):
		serializer = UserLoginSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user , token = serializer.save()
		data = {
			'profile':ProfileModelSerializer(user.profile).data,
			'user':UserModelSerializer(user).data,
			'access_token':token
		}
		return Response(data , status=status.HTTP_201_CREATED)


	@action(detail=False , methods=['post'])
	def signup(self, request):
		serializer = UserSignUpSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save()
		data = UserModelSerializer(user).data
		return Response(data , status=status.HTTP_201_CREATED)


	def retrieve(self , request , *args , **kwargs):
		#extrada
		response = super(UserViewSet , self).retrieve(request,*args , **kwargs)
		id_user = response.data.get('id')
		posts = Post.objects.filter(user=id_user).order_by('-created')
		data = {
			'user':response.data,
			'posts':PostModelSerializer(posts , many=True).data
		}
		response.data = data

		return response


