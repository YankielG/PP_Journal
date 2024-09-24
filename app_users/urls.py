from django.urls import path
from . import (views)

urlpatterns = [
    path('register', views.register, name='register_url'),
    path('password_reset', views.password_reset, name='password_reset_url'),
    path('password_change', views.password_change, name='password_change_url'),
    path('edit_profile', views.edit_profile, name='edit_profile_url'),
]
