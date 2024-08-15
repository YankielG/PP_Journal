from django.urls import path
from . import (views)

urlpatterns = [
    path('', views.all_pulses, name='all_pulses_url'),
    path('details/<int:id>', views.pulse_details, name='pulse_details_url'),
    path('delete/<int:id>', views.delete_pulse, name='delete_pulse_url'),
    path('delete/all', views.delete_all_pulse, name='delete_all_pulse_url'),
    path('edit/<int:id>', views.edit_pulse, name='edit_pulse_url'),
    path('add', views.add_pulse, name='add_pulse_url')
]
