from django.urls import path
from . import (views)

urlpatterns = [
    path('', views.all_weights, name='all_weights_url'),
    path('details/<int:id>', views.weight_details, name='weight_details_url'),
    path('delete/<int:id>', views.delete_weight, name='delete_weight_url'),
    path('delete/all', views.delete_all_weight, name='delete_all_weight_url'),
    path('edit/<int:id>', views.edit_weight, name='edit_weight_url'),
    path('add', views.add_weight, name='add_weight_url'),

    path('info/', views.info, name='info_url'),
    path('error/', views.error, name='error_url'),
    path('home/', views.home, name='home_url')

]
