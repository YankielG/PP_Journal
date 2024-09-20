from django.contrib import admin
from app_growth.models import Growth

class GrowthAdmin(admin.ModelAdmin):
    list_filter = ('growth', 'creation_date', 'update_date', 'comments', 'owner')
    date_hierarchy = 'creation_date'
    list_display = ('growth', 'creation_date', 'update_date', 'comments', 'owner')

# Register your models here.
admin.site.register(Growth, GrowthAdmin)