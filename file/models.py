import uuid

from django.db import models
from magic import magic
from rest_framework.exceptions import ValidationError


class AbstractFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=50, default="file")
    file = models.FileField()

    def save(self, *args, **kwargs):
        type = magic.from_buffer(self.file.read(), mime=True)
        file_type = type.split('/')[0]
        print('ffffffffffffffffffffffff', file_type)
        if file_type == 'video' or file_type == 'image':
            self.type = type
            super().save(*args, **kwargs)
        else:
            raise ValidationError('%s is not image or video' % self.file)
