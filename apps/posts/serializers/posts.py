
"""posts serializers"""

#django rf
from rest_framework import serializers
from apps.posts.models import (Post , Comment)




class PostModelSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = (
			'id','photo' , 'user' ,'profile' , 'title' , 'likes' , 'numLikes' , 'numComments'
		)

		read_only_fields = (
			'id' , 'user' ,'profile' ,
		)

		depth = 1


class CommentsPostModelSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = (
			'id' , 'post' , 'user' , 'profile' ,'content'  , 'created'
		)

		read_only_fields = (
			'id' , 'user' , 'profile'
		)

		depth = 1


class CreateLikeSerializer(serializers.ModelSerializer):

	class Meta:
		model = Post
		fields = (
			'id' , 'likes'
		)

	def update(self , instance , data):
		"""update model serializer"""
		post = self.context['post']
		user = self.context['user']

		if post.likes.filter(pk=self.context['user']).exists():
			post.likes.remove(user)
			post.numLikes -= 1
			post.save()
			return post
		else:
			post.likes.add(user)
			post.numLikes += 1
			post.save()
			return post

		


class CreateCommentSerializer(serializers.ModelSerializer):

	
	class Meta:

		model = Comment
		fields = (
			 'id','profile' ,'content'  , 'created' , 'user' ,
		)

		

	def create(self , data):
		post = self.context['post']
		comentario = Comment.objects.create(**data , post=post)



		post.numComments += 1
		post.save()
		comentario.user = self.context['user']
		comentario.profile = self.context['profile']
		comentario.save()

		return comentario






