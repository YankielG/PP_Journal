from django import forms
from django.core.validators import MinValueValidator, RegexValidator, MaxValueValidator, MinLengthValidator
from django.forms.utils import ErrorList
from django.core.exceptions import ValidationError
from . import models
from datetime import datetime, timedelta

from .models import UserProfile, LoginHistory
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test

def validate_date(value):
    if value.date() < datetime.now().date() - timedelta(weeks=5200):
        raise ValidationError(f'{value} nie jest datą max 100 lat wstecz')


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class RegisterUserDetailsForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['birthday', 'gender']


class LoginHistoryForm(forms.ModelForm):
    class Meta:
        model = LoginHistory
        fields = ['user_agent', 'session_id']


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class EditUserDetailsForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['birthday', 'gender']


class EditUserPasswordForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']


class CustomLoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False)
