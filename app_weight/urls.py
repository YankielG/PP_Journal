from django.urls import path
from . import (views)

urlpatterns = [
    path('', views.all_weights, name='all_weights_url'),
    path('details/<int:id>', views.weight_details, name='weight_details_url'),
    path('info/', views.info, name='info_url'),
    path('error/', views.error, name='error_url'),
    path('home/', views.home, name='home_url')

]
