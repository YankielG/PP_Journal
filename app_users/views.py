from datetime import datetime, timedelta
from functools import wraps
from lib2to3.fixes.fix_input import context

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound, HttpResponseForbidden, HttpResponseRedirect
# from .forms import RegisterForm
from django.db.models import Avg, Min, Max, Count

from django.core.paginator import Paginator

from django.contrib.auth.models import User
from .models import UserProfile, LoginHistory
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import update_session_auth_hash, get_user_model, authenticate, login, logout

from django.contrib import messages

from .forms import RegisterUserForm, RegisterUserDetailsForm, EditUserForm, EditUserPasswordForm, EditUserDetailsForm
from .forms import LoginHistoryForm, CustomLoginForm


def LoginView(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if form.cleaned_data['remember_me']:
                request.session.set_expiry(604800)  # 1 tydznień
            else:
                request.session.set_expiry(0)  # Sesja przeglądarki
            return redirect('home_url')
    else:
        form = CustomLoginForm()
    return render(request, 'registration/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        register_user_form = RegisterUserForm(request.POST)
        register_profile_form = RegisterUserDetailsForm(request.POST)

        if register_user_form.is_valid() and register_profile_form.is_valid():
            user = register_user_form.save(commit=False)
            user.first_name = register_user_form.cleaned_data['first_name']
            user.last_name = register_user_form.cleaned_data['last_name']
            user.email = register_user_form.cleaned_data['email']
            user.save()

            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.birthday = register_profile_form.cleaned_data['birthday']
            profile.gender = register_profile_form.cleaned_data['gender']
            profile.save()
            # login(request, user)
            # messages.success(request, 'Twój profil został pomyślnie utworzony.')
            return redirect('login')

    context = {
        'time_value': datetime.now().strftime("%Y-%m-%d"),
        'time_max': datetime.now().strftime("%Y-%m-%d"),
        'time_min': (datetime.now() - timedelta(weeks=5200)).strftime("%Y-%m-%d"),
        'register_user_form': RegisterUserForm(),
        'register_profile_form': RegisterUserDetailsForm(),
    }
    return render(request, 'users/register.html', context)


def password_reset(request):
    logged_user = request.user
    if request.method == 'POST':
        return render(request, 'password_reset_done.html')

    return render(request, 'password_reset.html')


@login_required
def password_change(request):
    logged_user = request.user
    if request.method == 'POST':
        form = EditUserPasswordForm(user=logged_user, data=request.POST)
        if form.is_valid():
            logged_user = form.save()
            update_session_auth_hash(request, logged_user)
            messages.warning(request, 'Twoje hasło zostało pomyślnie zaktualizowane !')
            # logout(request)
            return redirect('profile_details_url')
    else:

        form = EditUserPasswordForm(user=logged_user)

    return render(request, 'password_change.html', {'form': form})


@login_required
def edit_profile(request):
    logged_user = request.user
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form_Edit_user = EditUserForm(request.POST, instance=logged_user)
        form_edit_user_details = EditUserDetailsForm(request.POST, instance=user_profile)

        if form_Edit_user.is_valid() and form_edit_user_details.is_valid():
            form_Edit_user.save()
            form_edit_user_details.save()
            messages.warning(request, 'Twoje dane zostały pomyślnie zaktualizowane !')
            return redirect('profile_details_url')

    context = {
        'user': logged_user,
        'time_value': logged_user.userprofile.birthday.strftime("%Y-%m-%d"),
        'time_max': datetime.now().strftime("%Y-%m-%d"),
        'time_min': (datetime.now() - timedelta(weeks=5200)).strftime("%Y-%m-%d"),
        'form_Edit_user': EditUserForm(instance=logged_user),
        'form_edit_user_details': EditUserDetailsForm(instance=user_profile),
    }
    return render(request, 'edit_profile.html', context)


@login_required
def profile_details(request):
    logged_user = request.user

    context = {
        'user': logged_user,
        'register_user_form': RegisterUserForm(),
        'register_profile_form': RegisterUserDetailsForm(),
    }
    return render(request, 'profile_details.html', context)

@login_required
def delete_profile(request):
    logged_user = request.user
    if request.method == 'POST':
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']
        user_pass = authenticate(username=logged_user, password=pass1)
        if pass1 == pass2 and user_pass is not None:
            logged_user.delete()
            messages.success(request, 'Twój profil został pomyślnie usunięty.')
            return redirect('login')
        else:
            messages.error(request, 'Nieprawidłowe hasło. Spróbuj ponownie')
            return redirect('profile_details_url')

    return render(request, 'delete_profile.html')


@login_required
def history(request):
    logged_user = request.user

    filter_value = request.GET.get('search')

    if filter_value and len(filter_value) > 2:
        found_history = LoginHistory.objects.filter(user=logged_user, ip_address__contains = filter_value).order_by('-ip_address')
    else:
        found_history = LoginHistory.objects.filter(user=logged_user).order_by('-login_date')

    page_num = request.GET.get('page', 1)
    pages = Paginator(found_history, 8)

    pages_max = pages.num_pages
    pages_max_elements = pages.count
    page_results = pages.get_page(page_num)

    context = {
        'filter_value': filter_value,
        'pages_max': pages_max,
        'pages_max_elements': pages_max_elements,
        'history': page_results,
        'user': logged_user,
    }
    return render(request, 'history.html', context)