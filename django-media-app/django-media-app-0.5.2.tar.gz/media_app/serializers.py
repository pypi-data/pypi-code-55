from rest_framework import serializers

from .models import Media


class AvatarMixin(serializers.Serializer):
    avatar = serializers.SerializerMethodField(read_only=True)
    avatar_file = serializers.FileField(write_only=True, required=False)

    def get_avatar(self, obj):
        if obj.cover is not None:
            return ImageSerializer(obj.avatar, context=self.context).data
        return None

    class Meta:
        fields = ('avatar', 'avatar_file')


class CoverMixin(serializers.Serializer):
    cover = serializers.SerializerMethodField(read_only=True)
    cover_file = serializers.FileField(write_only=True, required=False)

    def get_cover(self, obj):
        if obj.cover is not None:
            return ImageSerializer(obj.cover, context=self.context).data
        return None

    class Meta:
        fields = ('cover', 'cover_file')


class GalleryMixin(serializers.Serializer):
    gallery = serializers.SerializerMethodField(read_only=True)
    gallery_files = serializers.FileField(write_only=True, required=False)

    def get_gallery(self, obj):
        if not obj.gallery or obj.gallery.count()==0:
            return None
        return ImageSerializer(obj.gallery, context=self.context, many=True).data

    class Meta:
        fields = ('gallery', 'gallery_files')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ('file', 'thumbnail',)
