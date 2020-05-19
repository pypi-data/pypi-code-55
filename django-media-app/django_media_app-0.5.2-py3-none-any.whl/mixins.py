from django.contrib.contenttypes.models import ContentType

from .models import Media


class MediaMixin:

    def __queryset(self):
        content_type = ContentType.objects.get_for_model(self)
        try:
            return Media.objects.filter(content_type=content_type, object_id=self.id)
        except:
            return None

    def get_media(self, **kwargs):
        return self.__queryset().filter(**kwargs)

    def get_avatars(self):
        return self.get_media(position=Media.POSITION_AVATAR, type=Media.TYPE_IMAGE)

    def get_covers(self):
        return self.get_media(position=Media.POSITION_COVER, type=Media.TYPE_IMAGE)

    def get_attachments(self):
        return self.get_media(position=Media.POSITION_ATTACHMENT)

    def get_images(self):
        return self.get_media(type=Media.TYPE_IMAGE)

    def get_videos(self):
        return self.get_media(type=Media.TYPE_VIDEO)

    def get_documents(self):
        return self.get_media(type=Media.TYPE_DOCUMENT)

    def get_other_files(self):
        return self.get_media(type=Media.TYPE_OTHER)

    @property
    def avatar(self):
        return self._avatar

    @property
    def cover(self):
        return self._cover

    @property
    def image(self):
        return self._image

    def add_media(self, *files, type=Media.TYPE_OTHER, position=Media.POSITION_ATTACHMENT, group=None):
        content_type = ContentType.objects.get_for_model(self)
        media_list = []
        for file in files:
            media = Media(group=group,
                          position=position,
                          type=type,
                          content_type=content_type,
                          object_id=self.id,
                          file=file)
            media.save()
            media_list.append(media)
        return media_list

    @image.setter
    def image(self, file):
        image = self.add_media(file, type=Media.TYPE_IMAGE, position=Media.POSITION_ATTACHMENT)[0]
        self._image = image

    @cover.setter
    def cover(self, file):
        cover = self.add_media(file, type=Media.TYPE_IMAGE, position=Media.POSITION_COVER)[0]
        self._cover = cover

    @avatar.setter
    def avatar(self, file):
        avatar = self.add_media(file, type=Media.TYPE_IMAGE, position=Media.POSITION_AVATAR)[0]
        self._avatar = avatar
