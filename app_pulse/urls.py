from django.urls import path
from . import (views)

urlpatterns = [
    path('', views.all_pulses, name='all_pulses_url')
]
