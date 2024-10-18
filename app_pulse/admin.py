from django.contrib import admin
from app_pulse.models import Pulse

class PulseAdmin(admin.ModelAdmin):
    list_filter = ('pulse', 'creation_date', 'update_date', 'cnt_modification', 'comments', 'owner')
    date_hierarchy = 'creation_date'
    list_display = ('pulse', 'creation_date', 'update_date', 'cnt_modification', 'comments', 'owner')

# Register your models here.
admin.site.register(Pulse, PulseAdmin)