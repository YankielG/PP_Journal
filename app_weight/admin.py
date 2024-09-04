from django.contrib import admin
from app_weight.models import Weight

class WeightAdmin(admin.ModelAdmin):
    list_filter = ('weight', 'comments')
    date_hierarchy = 'date'
    list_display = ('weight', 'date', 'comments')

# Register your models here.
admin.site.register(Weight, WeightAdmin)