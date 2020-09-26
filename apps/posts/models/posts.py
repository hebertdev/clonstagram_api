"""Posts models."""

# Django
from django.db import models
from apps.users.models import User , Profile



class Post(models.Model):
    """Post model."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='posts/photos' , blank=False , null=False)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    numLikes = models.IntegerField('Numero de likes' , default=0)
    numComments = models.IntegerField('Numero de comentarios' , default=0)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return title and username."""
        return '{} by @{}'.format(self.title, self.user.username)


class Comment(models.Model):
    post = models.ForeignKey(Post , on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} by @{}'.format(self.post.title, str(self.user.username))