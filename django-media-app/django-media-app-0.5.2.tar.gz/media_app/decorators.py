from .models import Media


def media_serializer(is_create=True, avatar_column="avatar_file", cover_column="cover_file",
                     images_column="image_files"):
    def media_serializer_decorator(func):
        def inner(*args, **kwargs):
            validated_data = args[1] if is_create else args[2]
            # pop medial files to handle it

            avatar = validated_data.pop(avatar_column, None)
            cover = validated_data.pop(cover_column, None)
            is_images = validated_data.pop(images_column, None)  # remove
            images = None
            if is_images is not None:
                images = args[0].context["request"].data.getlist(images_column, None)
            # call create or update method of serializer
            instance = func(*args, **kwargs)

            if avatar is not None:
                instance.avatar = avatar
            if cover is not None:
                instance.cover = cover
            if images is not None:
                instance.add_media(*images, type=Media.TYPE_IMAGE, position=Media.POSITION_ATTACHMENT)
            #  save if there is any changes in media files
            if cover is not None or avatar is not None:
                instance.save()

            return instance

        return inner

    return media_serializer_decorator
