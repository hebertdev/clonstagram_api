from django.contrib.auth import authenticate , password_validation




from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

from apps.users.models import User , Profile


from apps.users.serializers.profiles import ProfileModelSerializer



class UserModelSerializer(serializers.ModelSerializer):

	profile = ProfileModelSerializer(read_only=True)

	class Meta:
		model = User
		fields = (
			'id',
			'username',
			'first_name',
			'last_name',
			'email',
			'profile',
		)



class UserSignUpSerializer(serializers.Serializer):
	"""user signup serializer"""
	email = serializers.EmailField(
		validators=[
			UniqueValidator(queryset=User.objects.all())
		]
	)
	username = serializers.CharField(
		min_length=4,
		max_length=20,
		validators=[
			UniqueValidator(queryset=User.objects.all())
		]
	)

	first_name = serializers.CharField(min_length=2 , max_length=30)
	last_name = serializers.CharField(min_length=2 , max_length=30)
	password = serializers.CharField(min_length=8 , max_length=64)
	password_confirmation = serializers.CharField(min_length=8 , max_length=64)


	def validate(self , data):
		passwd = data['password']
		passwd2 = data['password_confirmation']

		if passwd != passwd2:
			raise serializers.ValidationError('Las contraseñas no coinciden')
		password_validation.validate_password(passwd)
		return data
	def create(self, data):
		data.pop('password_confirmation')
		user = User.objects.create_user(**data)
		return user

class UserLoginSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField(min_length=8 , max_length=64)

	def validate(self, data):
		#verified credentials
		user = authenticate(username=data['email'] , password=data['password'])

		if not user:
			raise serializers.ValidationError('invalid credentials')

		self.context['user'] = user
		self.context['profile'] = user.profile
		return data

	def create(self,data):
		token , created = Token.objects.get_or_create(user=self.context['user'])
		return self.context['user'], token.key





class FollowSerializer(serializers.ModelSerializer):

	
	class Meta:
		model = User
		fields = (
			'profile', 
		)


	def update(self , instance , data):
		"""update model serializer"""
		user_to_follow =  self.context['user_to_follow'] 
		user = self.context['user']
		seguidores = user_to_follow.profile.followers.count()


		if user_to_follow.profile.followers.filter(pk=user.id).exists():
			user_to_follow.profile.followers.remove(user.pk)
			user_to_follow.profile.numFollowers -= 1
			user_to_follow.profile.save()
			user.profile.numFolloweds -= 1
			user.profile.save()
			user_to_follow.save()
			return user_to_follow
		else:
			user_to_follow.profile.followers.add(user.pk)
			user_to_follow.profile.numFollowers += 1
			user_to_follow.profile.save()
			user.profile.numFolloweds += 1
			user.profile.save()
			user_to_follow.save()
			return user_to_follow
		
		