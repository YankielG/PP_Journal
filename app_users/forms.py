from django import forms
from django.core.validators import MinValueValidator, RegexValidator, MaxValueValidator, MinLengthValidator
from django.forms.utils import ErrorList
from django.core.exceptions import ValidationError
from . import models
from datetime import datetime, timedelta

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test

def validate_date(value):
    if value.date() < datetime.now().date() - timedelta(weeks=5200):
        raise ValidationError(f'{value} nie jest datą max 100 lat wstecz')

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']



class Add_users_form(forms.Form):
    user = forms.CharField(max_length=20)
    creation_date = forms.DateTimeField(label='Data wpisu', validators=[validate_date], widget=forms.DateTimeInput(attrs={'class': 'datepicker', 'type': datetime}), initial=datetime.now().strftime("%Y-%m-%dT%H:%M")),
    update_date = forms.DateTimeField(label='Data aktualizacji', validators=[validate_date], widget=forms.DateTimeInput(attrs={'class': 'datepicker', 'type': datetime}), initial=datetime.now().strftime("%Y-%m-%dT%H:%M")),
    comments = forms.CharField(label='Uwagi', max_length=255, validators=[MinLengthValidator(2)], widget=forms.Textarea(attrs={'class': 'form-control', 'maxlength': 150, 'rows': 5, })),
    owner = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput(), required=False)



    def __str__(self):
        return f'Użytkownik: {self.user} Data: {self.date} Uwagi: {self.comments}'