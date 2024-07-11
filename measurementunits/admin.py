from django.contrib import admin
from .models import MeasurementUnit

@admin.register(MeasurementUnit)
class MeasurementUnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'volume_in_ml', 'created_at', 'updated_at')
    search_fields = ('name',)
