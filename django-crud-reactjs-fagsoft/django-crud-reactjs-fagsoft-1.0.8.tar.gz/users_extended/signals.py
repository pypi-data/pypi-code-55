from django.db.models.signals import pre_delete, post_init, post_save
from django.dispatch import receiver

from .models import ExtendedUser


@receiver(pre_delete, sender=ExtendedUser)
def profile_image_pre_delete(sender, instance, **kwargs):
    instance.profile_image.delete(False)


@receiver(post_init, sender=ExtendedUser)
def backup_profile_image_path(sender, instance, **kwargs):
    instance._current_profile_image = instance.profile_image


@receiver(post_save, sender=ExtendedUser)
def delete_profile_image(sender, instance, **kwargs):
    if hasattr(instance, '_current_profile_image'):
        if instance._current_profile_image != instance.profile_image:
            instance._current_profile_image.delete(save=False)
