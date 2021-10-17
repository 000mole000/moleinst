import uuid
import magic
from django.core.exceptions import ValidationError

from django.db import models
from django.contrib.auth.models import User

from file.models import AbstractFile


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    publish_date = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class PostFile(AbstractFile, models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='files')


class Comment(models.Model):
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    publish_date = models.DateTimeField(auto_now_add=True)


class Report(models.Model):
    REPORT_CHOICES = [
        ('Spam', 'Spam'),
        ('Inappropriate', 'Inappropriate content'),
        ('Other', 'Other'),
    ]
    type = models.CharField(max_length=30, choices=REPORT_CHOICES, default='Spam')
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reports')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    publish_date = models.DateTimeField(auto_now_add=True)


class AlertConnect(models.Model):
    alert_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="alerts")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="alert_users")
    new_posts_count = models.PositiveIntegerField(default=0)
