import io
import uuid
import qrcode
from django.db import models
from django.core.files import File


class QRCodeMixin(models.Model):
    class Meta:
        abstract = True

    qr_version = 1
    qr_error_correction = qrcode.constants.ERROR_CORRECT_L
    qr_box_size = 10
    qr_border = 4
    qrcode = models.ImageField(upload_to='qrcode', blank=True, null=True, editable=False)

    def get_qrcode_data(self):
        return self.id

    def get_qrcode_filename(self):
        return "%s_%s_%s.png" % (self._meta.app_label, self._meta.model_name, self.pk or uuid.uuid4())

    def make_image(self):
        qr = qrcode.QRCode(
            version=self.qr_version,
            error_correction=self.qr_error_correction,
            box_size=self.qr_box_size,
            border=self.qr_border
        )
        qr.add_data(self.get_qrcode_data())
        return qr.make_image()

    def generate_qrcode(self):
        stream = io.BytesIO()
        self.make_image().save(stream, format='PNG')
        self.qrcode.save(self.get_qrcode_filename(), File(stream), save=False)
        stream.close()

    def save(self, *args, **kwargs):
        if not self.qrcode:
            self.generate_qrcode()
        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        self.qrcode.delete(save=False)
        super().delete(using=using, keep_parents=keep_parents)
