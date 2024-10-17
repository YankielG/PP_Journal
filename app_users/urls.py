from django.urls import path
from . import (views)

urlpatterns = [
    path('register', views.register, name='register_url'),
    path('password_reset', views.password_reset, name='password_reset_url'),
    path('password_change', views.password_change, name='password_change_url'),
    path('profile_details', views.profile_details, name='profile_details_url'),
    path('edit_profile', views.edit_profile, name='edit_profile_url'),
    path('delete_profile/', views.delete_profile, name='delete_profile_url'),
    path('history', views.history, name='history_url'),
    path('login', views.LoginView, name='login_url'),
]
