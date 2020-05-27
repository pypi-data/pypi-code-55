from django.contrib import admin
from django.utils.html import format_html

class QRCodeAdminMixin(admin.ModelAdmin):

    def qrcode_thumbnail(self, obj):
        return format_html("<img src='%s' style='height:32px; width='32px' />" % obj.qrcode.url)

    def get_list_display(self, request):
        list_display = super(QRCodeAdminMixin, self).get_list_display(request)
        return ['qrcode_thumbnail'] + list_display