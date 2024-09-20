from django.contrib import admin
from app_pressure.models import  Pressure

class PressureAdmin(admin.ModelAdmin):
    list_filter = ('shrink', 'diastole', 'pulse', 'creation_date', 'update_date', 'comments', 'owner')
    date_hierarchy = 'creation_date'
    list_display = ('shrink', 'diastole', 'pulse', 'creation_date', 'update_date', 'comments', 'owner')

# Register your models here.
admin.site.register(Pressure, PressureAdmin)