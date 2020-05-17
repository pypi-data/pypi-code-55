from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from emailuser import models


class UserAdmin(BaseUserAdmin):
    ordering = ['email']
    search_fields = ('email', 'first_name', 'last_name', 'username',
                     'joined_date')
    list_display = ['email', 'username', 'first_name', 'last_name', 'is_staff']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {
         'fields': ('first_name', 'last_name', 'username')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login', 'joined_date')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'username')
        }),
    )


admin.site.register(models.User, UserAdmin)
