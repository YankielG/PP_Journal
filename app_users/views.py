from datetime import datetime, timedelta
from functools import wraps

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound, HttpResponseForbidden, HttpResponseRedirect
# from .forms import RegisterForm
from django.db.models import Avg, Min, Max, Count

from django.core.paginator import Paginator

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from sqlalchemy.testing.suite.test_reflection import users

from .forms import RegisterForm

def register(request):

    if request.method  == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_data = register_form.cleaned_data
            user = register_form.save(commit=False)
            user.first_name = user_data['first_name']
            user.last_name = user_data['last_name']
            user.email = user_data['email']
            user.save()
            return redirect('login')

    context = {
        'time_value': datetime.now().strftime("%Y-%m-%d"),
        'time_max': datetime.now().strftime("%Y-%m-%d"),
        'time_min': (datetime.now() - timedelta(weeks=5200)).strftime("%Y-%m-%d"),
        'register_form': RegisterForm()
    }
    return render(request, 'users/register.html', context)

def password_reset(request):
    logged_user = request.user
    if request.method == 'POST':
        return  render(request, 'password_reset_done.html')

    return  render(request, 'password_reset.html')

@login_required
def password_change(request):
    logged_user = request.user
    return  render(request, '404.html')

@login_required
def edit_profile(request):
    logged_user = request.user
    if request.method  == 'POST':
        register_form = RegisterForm(request.POST, instance=logged_user)
        logged_user.save()
        if register_form.is_valid():
            user_data = register_form
            print(user_data)
            user = register_form.save(commit=False)
            user.id = user_data['id']
            user.first_name = user_data['first_name']
            user.last_name = user_data['last_name']
            user.email = user_data['email']
            user.save()
            return redirect('profile_details_url')

    context = {
        'user': logged_user,
        'gender': 'man',
        'time_value': datetime.now().strftime("%Y-%m-%d"),
        'time_max': datetime.now().strftime("%Y-%m-%d"),
        'time_min': (datetime.now() - timedelta(weeks=5200)).strftime("%Y-%m-%d"),
        'register_form': RegisterForm(instance=logged_user)
    }
    return render(request, 'edit_profile.html', context)

@login_required
def profile_details(request):
    logged_user = request.user
    gender = "Mężczyzna"
    context = {
        'user': logged_user,
        'gender': gender,
        'time_value': datetime.now().strftime("%Y-%m-%d"),
        'time_max': datetime.now().strftime("%Y-%m-%d"),
        'time_min': (datetime.now() - timedelta(weeks=5200)).strftime("%Y-%m-%d"),
        'register_form': RegisterForm()
    }
    return render(request, 'profile_details.html', context)