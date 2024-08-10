from django.urls import path
from . import (views)

urlpatterns = [
    path('', views.all_pressures, name='all_pressures_url')
]
