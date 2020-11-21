from django.db import models
from django.conf import settings
from django.utils import timezone
# Create your models here.

User = settings.AUTH_USER_MODEL


class Post(models.Model):
    image = models.ImageField(
        upload_to='posts/', null=True, default='posts/no-img.jpg')
    content = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, related_name='user',
                             default=1, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content


class Like(models.Model):
    user = models.ForeignKey(User, related_name='likes',
                             null=True, blank=True, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes',
                             null=True, blank=True, on_delete=models.CASCADE)


class Comment(models.Model):
    user = models.ForeignKey(User, related_name='comments',
                             null=False, default=1, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments',
                             null=False, default=1, on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ImageField(
        upload_to='posts/', null=True, default='posts/no-img.jpg')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text


class CommentReplies(models.Model):
    user = models.ForeignKey(User, related_name='commentReplies',
                             null=False, default=1, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, related_name='commentReplies',
                                null=False, default=1, on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ImageField(
        upload_to='posts/', null=True, default='posts/no-img.jpg')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text


class CommentLike(models.Model):
    user = models.ForeignKey(User, related_name='commentlikes',
                             null=True, blank=True, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, related_name='commentlikes',
                                null=True, blank=True, on_delete=models.CASCADE)
