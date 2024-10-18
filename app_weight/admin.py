from django.contrib import admin
from app_weight.models import Weight

class WeightAdmin(admin.ModelAdmin):
    list_filter = ('weight', 'creation_date', 'update_date', 'cnt_modification', 'comments', 'owner')
    date_hierarchy = 'creation_date'
    list_display = ('weight', 'creation_date', 'update_date', 'cnt_modification', 'comments', 'owner')

# Register your models here.
admin.site.register(Weight, WeightAdmin)