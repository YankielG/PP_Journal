from django.contrib import admin
from app_growth.models import Growth

class GrowthAdmin(admin.ModelAdmin):
    list_filter = ('growth', 'comments')
    date_hierarchy = 'date'
    list_display = ('growth', 'date', 'comments')

# Register your models here.
admin.site.register(Growth, GrowthAdmin)