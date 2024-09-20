from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound, HttpResponseForbidden
# from .forms import RegisterForm
from django.db.models import Avg, Min, Max, Count

from django.core.paginator import Paginator

from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import RegisterForm

def register(request):

    if request.method == 'GET':
        register_form = RegisterForm()
        context = {
            'register_form': register_form
        }
        return render(request, 'users/register.html', context)

    register_form = RegisterForm(request.POST)
    if register_form.is_valid():
        user_data = register_form.cleaned_data
        user = register_form.save(commit=False)
        user.first_name = user_data['first_name']
        user.last_name = user_data['last_name']
        user.email = user_data['email']
        user.save()
        return redirect('login')
    else:
        context = {
            'register_form': register_form
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

