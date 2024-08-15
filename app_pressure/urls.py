from django.urls import path
from . import (views)

urlpatterns = [
    path('', views.all_pressures, name='all_pressures_url'),
    path('details/<int:id>', views.pressure_details, name='pressure_details_url'),
    path('delete/<int:id>', views.delete_pressure, name='delete_pressure_url'),
    path('delete/all', views.delete_all_pressure, name='delete_all_pressure_url'),
    path('edit/<int:id>', views.edit_pressure, name='edit_pressure_url'),
    path('add', views.add_pressure, name='add_pressure_url')
]
