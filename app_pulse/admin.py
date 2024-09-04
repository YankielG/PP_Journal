from django.contrib import admin
from app_pulse.models import Pulse

class PulseAdmin(admin.ModelAdmin):
    list_filter = ('pulse', 'comments')
    date_hierarchy = 'date'
    list_display = ('pulse', 'date', 'comments')

# Register your models here.
admin.site.register(Pulse, PulseAdmin)