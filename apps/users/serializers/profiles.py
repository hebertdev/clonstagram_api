
from django.contrib.auth import authenticate , password_validation

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

from apps.users.models import User , Profile




class ProfileModelSerializer(serializers.ModelSerializer):
    """Profile model serializer."""
    class Meta:
        """Meta class."""

        model = Profile
        fields = (
            'avatar',
            'bio',
            'link',
            'followers',
            'numFollowers',
            'numFolloweds',
        )
        read_only_fields = (
            'user',
            'followers',
        )

        depth = 1