from django.contrib import admin
from .models import PersonModel, OrganizationModel

# Register your models here.

@admin.register(PersonModel)
class PersonAdmin(admin.ModelAdmin):
    pass

@admin.register(OrganizationModel)
class OrganizationAdmin(admin.ModelAdmin):
    pass


