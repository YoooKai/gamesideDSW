from django.contrib import admin
from .models import Platform
# Register your models here.
@admin.register(Platform)
class PlatformsAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
        'description',
        'logo',
    )

    prepopulated_fields = {'slug': ['name']}