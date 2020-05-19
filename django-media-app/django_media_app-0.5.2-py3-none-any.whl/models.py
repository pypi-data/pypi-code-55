import os
import uuid
from datetime import date

import magic
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext as _
from .utils import resize_image

def prepare_name(folder_name, filename):
    extension = os.path.splitext(filename)[1]
    date_part = date.today().strftime("%Y-%m-%d")
    result = os.path.join(os.path.join(folder_name, date_part), str(uuid.uuid4()) + extension)
    return result

class Media(models.Model):
    POSITION_AVATAR = "avatar"
    POSITION_COVER = "cover"
    POSITION_ATTACHMENT = "attachment"

    TYPE_IMAGE = "image"
    TYPE_VIDEO = "video"
    TYPE_DOCUMENT = "document"
    TYPE_OTHER = "other"

    POSITIONS_LIST = (
        (POSITION_AVATAR, _("Avatar")),
        (POSITION_COVER, _("Cover")),
        (POSITION_ATTACHMENT, _("Attachment")),
    )
    TYPES_LIST = (
        (TYPE_IMAGE, _("Image")),
        (TYPE_VIDEO, _("Video")),
        (TYPE_DOCUMENT, _("Document")),
        (TYPE_OTHER, _("Other")),
    )

    def upload_to_media(self, filename):
        filename = prepare_name(self.content_type.model, filename)
        if self.mime_type.split("/")[0] == "image":
            self.thumbnail = resize_image(self.file, size=(256, 256), path=filename)
        return filename

    title = models.CharField(max_length=255)
    type = models.CharField(max_length=31, default=TYPE_OTHER, choices=TYPES_LIST)
    position = models.CharField(max_length=31, default=POSITION_ATTACHMENT, choices=POSITIONS_LIST)
    file = models.FileField(upload_to=upload_to_media)
    thumbnail = models.ImageField(null=True)
    mime_type = models.CharField(max_length=127)
    size = models.BigIntegerField(null=True)
    group = models.CharField(max_length=255, null=True, blank=True)
    # generic foreign key
    object_id = models.IntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, )
    content_object = GenericForeignKey('content_type', 'object_id', )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        self.title = os.path.splitext(self.file.name)[0]
        self.size = self.file.size
        self.mime_type = magic.from_buffer(self.file.read(), mime=True)
        file_type = self.mime_type.split("/")[0]
        if self.type == self.TYPE_IMAGE and file_type != "image":
            raise ValidationError(_('This file is not an image'))
        if self.type == self.TYPE_VIDEO and file_type != "video":
            raise ValidationError(_('This file is not a video'))

    class Meta:
        verbose_name = _("Media")
        verbose_name_plural = _("Media")
        db_table = "media"
        indexes = [
            models.Index(fields=['type', 'position']),
        ]

    def save(self, *args, **kwargs):
        self.clean()
        super(Media, self).save(*args, **kwargs)
