from django.contrib import admin
from .models import PersonModel, OrganizationModel, BusinessFormModel, DependenceQualityModel, DependenceLegitimacyModel

# Register your models here.


@admin.register(DependenceLegitimacyModel)
class DependenceLegitimacyAdmin(admin.ModelAdmin):
    pass

@admin.register(DependenceQualityModel)
class DependenceQualityAdmin(admin.ModelAdmin):
    pass

@admin.register(BusinessFormModel)
class BusinessFormAdmin(admin.ModelAdmin):
    pass



@admin.register(PersonModel)
class PersonAdmin(admin.ModelAdmin):
    pass

@admin.register(OrganizationModel)
class OrganizationAdmin(admin.ModelAdmin):
    pass


