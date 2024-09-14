from django.urls import path
from . import (views)

urlpatterns = [
    path('', views.home, name='home_url'),
    path('info', views.info, name='info_url'),
    path('info/', views.info, name='info_url'),
    path('error/', views.error, name='error_url'),
    path('home/', views.home, name='home_url'),
]

