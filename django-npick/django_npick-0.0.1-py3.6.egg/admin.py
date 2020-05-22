from django.contrib import admin

from .forms import IconForm
from .models import Icon


class IconAdmin(admin.ModelAdmin):
    '''example'''
    form = IconForm
    list_display = ['name']


admin.site.register(Icon, IconAdmin)
