from django.contrib import admin
from app_pressure.models import  Pressure

class PressureAdmin(admin.ModelAdmin):
    list_filter = ('shrink', 'diastole', 'pulse', 'comments')
    date_hierarchy = 'date'
    list_display = ('shrink', 'diastole', 'pulse', 'date', 'comments')

# Register your models here.
admin.site.register(Pressure, PressureAdmin)