from django.urls import path
from . import (views)

urlpatterns = [
    path('', views.all_growths, name='all_growths_url')
]
