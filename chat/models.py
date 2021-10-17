import uuid

from django.contrib.auth.models import User
from django.db import models
from magic import magic
from rest_framework.exceptions import ValidationError

from file.models import AbstractFile


class Dialog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class DialogMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE)


class Message(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE)


class MessageFile(AbstractFile, models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='files')