from datetime import datetime, timedelta
from functools import wraps
from lib2to3.fixes.fix_input import context

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound, HttpResponseForbidden, HttpResponseRedirect
# from .forms import RegisterForm
from django.db.models import Avg, Min, Max, Count

from django.core.paginator import Paginator

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import update_session_auth_hash
from pyexpat.errors import messages
from sqlalchemy.testing.suite.test_reflection import users

from .forms import RegisterForm, UserProfileForm, UserPasswordForm


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
    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password1 = request.POST['password1']
        new_password2 = request.POST['password2']

        if not logged_user.check_password(old_password):
            context = {
                'messages': 'Błędne stare hasło'
            }
            return  render(request, 'password_change.html', context)

        if old_password == new_password1:
            context = {
                'messages': 'Nowe hasło takie samo jak stare'
            }
            return  render(request, 'password_change.html', context)
        if new_password1 != new_password2:
            context = {
                'messages': 'Nowe hasła nie są zgodne'
            }
            return  render(request, 'password_change.html', context)

        logged_user.set_password(new_password1)
        logged_user.save()
        update_session_auth_hash(request, logged_user)
        return redirect('profile_details_url')

    context = {
        'messages': '',
        'user': logged_user,
        'register_form': UserPasswordForm(instance=logged_user)
    }
    return  render(request, 'password_change.html', context)

@login_required
def edit_profile(request):
    logged_user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=logged_user)
        if form.is_valid():
            # logged_user.save()
            form.save()
            return redirect('profile_details_url')

    gender = 'man'
    context = {
        'user': logged_user,
        'gender': gender,
        'time_value': datetime.now().strftime("%Y-%m-%d"),
        'time_max': datetime.now().strftime("%Y-%m-%d"),
        'time_min': (datetime.now() - timedelta(weeks=5200)).strftime("%Y-%m-%d"),
        'register_form': UserProfileForm(instance=logged_user)
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
        'register_form': RegisterForm()
    }
    return render(request, 'profile_details.html', context)