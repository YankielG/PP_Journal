from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound, HttpResponseForbidden
# from .forms import RegisterForm
from django.db.models import Avg, Min, Max, Count

from django.core.paginator import Paginator

from django.contrib.auth.decorators import login_required, user_passes_test

def register(request):
    return  render(request, 'users/register.html')

def password_reset(request):
    if request.method == 'POST':
        return  render(request, 'password_reset_done.html')

    return  render(request, 'password_reset.html')

@login_required
def password_change(request):
    return  render(request, '404.html')

