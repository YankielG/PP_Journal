from django.urls import path
from . import (views)

urlpatterns = [
    path('register', views.register, name='register_url'),
    path('password_reset', views.password_reset, name='password_reset_url'),


]
