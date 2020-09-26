import sys
from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from apps.users.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.urls import reverse
from django.http import HttpResponse , HttpResponseRedirect , JsonResponse



class Profile(models.Model):
    """Profile model.

    A profile holds a user's public data like biography, picture,
    and statistics.
    """
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    avatar = models.ImageField(
        'profile picture',
        upload_to='users/pictures/',
        blank=True,
        null=True
    )
    followers = models.ManyToManyField('users.User', related_name='follower', blank=True)
    bio = models.TextField(max_length=200, blank=True)
    link = models.URLField(max_length=200 , blank=True)
    # Stats
    numFollowers = models.IntegerField('Numero de seguidores' , default=0)
    numFolloweds = models.IntegerField('Numero de sguidos' , default=0)


    def __str__(self):
        """Return user's str representation."""
        return str(self.user)


@receiver(post_save, sender=User)
def ensure_profile_exists(sender, instance, **kwargs):
    if kwargs.get('created', False):
        Profile.objects.get_or_create(user=instance)
        # print("Se acaba de crear un usuario y su perfil enlazado")

