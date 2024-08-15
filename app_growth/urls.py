from django.urls import path
from . import (views)

urlpatterns = [
    path('', views.all_growths, name='all_growths_url'),
    path('details/<int:id>', views.growth_details, name='growth_details_url'),
    path('delete/<int:id>', views.delete_growth, name='delete_growth_url'),
    path('delete/all', views.delete_all_growth, name='delete_all_growth_url'),
    path('edit/<int:id>', views.edit_growth, name='edit_growth_url'),
    path('add', views.add_growth, name='add_growth_url')
]
