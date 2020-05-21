# Register your models here.
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from db.models import Member, Tag, AdmonitionTemplate, License, Section, Book

AdminSite.site_header = _('Muses Administration')
AdminSite.site_title = _('Administration Site of Muses')


@admin.register(Member)
class MemberAdmin(UserAdmin):
    pass


@admin.register(Section)
class SectionAdmin(ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    pass


@admin.register(AdmonitionTemplate)
class AdmonitionTemplateAdmin(ModelAdmin):
    pass


@admin.register(License)
class LicenseAdmin(ModelAdmin):
    pass


@admin.register(Book)
class BookAdmin(ModelAdmin):
    pass
