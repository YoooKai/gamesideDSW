from django.contrib import admin
from .models import Order
# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'status',
        'created_at',
        'updated_at',
        'key',
        'user',
    )