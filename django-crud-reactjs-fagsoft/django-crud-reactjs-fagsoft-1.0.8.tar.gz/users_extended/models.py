from django.contrib.auth.models import User
from countries.models import City
import random
from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit


class ExtendedUser(models.Model):
    CHOICES_GENDER = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    )

    def profile_image_upload_to(self, filename) -> str:  # pragma: no cover
        nro_random = random.randint(1111, 9999)
        return "img/users/profile/%s01j%sj10%s.%s" % (self.id, nro_random, self.id, filename.split('.')[-1])

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='extended_user')
    # encrypted = models.BooleanField(default=False)
    alias = models.CharField(max_length=200, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(choices=CHOICES_GENDER, max_length=1, null=True, blank=True)
    profile_image = ProcessedImageField(
        processors=[ResizeToFit(300, 300)],
        format='PNG',
        options={'quality': 100},
        null=True,
        blank=True,
        upload_to=profile_image_upload_to
    )
    security_pin = models.CharField(max_length=300, null=True)
    security_qr = models.CharField(max_length=300, null=True)
    multi_sessions = models.BooleanField(default=False)
    multi_sessions_qty = models.PositiveIntegerField(default=0)
    registration_token = models.CharField(null=True, max_length=400)
    registration_expiration = models.DateField(null=True)
    city = models.ForeignKey(City, null=True, on_delete=models.PROTECT)

    @classmethod
    def encrypted_fields(cls):
        return ['first_name', 'last_name']


class UserAditionalPermission(models.Model):
    class Meta:
        managed = False
        permissions = (
            ('list_user', 'Can list user'),
            ('change_password_other_user', 'Can change other user password'),
            ('change_pin_other_user', 'Can change other user pin'),
            ('change_qr_other_user', 'Can change other user qr'),
            ('change_profile_other_user', 'Can change other user profile'),
            ('change_profile_image_other_user', 'Can change other user profile image'),
            ('change_profile_user', 'Can change user profile'),
            ('change_password_user', 'Can change user password'),
            ('change_pin_user', 'Can change user pin'),
            ('change_qr_user', 'Can change user qr'),
            ('change_profile_image_user', 'Can change user profile image'),
            ('change_permission_user', 'Can change user permission'),
            ('make_superuser_user', 'Can make user superuser'),
            ('make_staff_user', 'Can make user staff'),
            ('make_active_user', 'Can make user active'),
        )
