from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from django.contrib.auth.models import User

def validate_date(value):
    if value.date() < datetime.now().date() - timedelta(weeks=5200):
        raise ValidationError(f'{value} nie jest datą max 1 rok wstecz')

def validate_date_only(value):
    if value.date() < (datetime.now() - timedelta(weeks=5200)).date():
        raise ValidationError(f'{value} nie jest datą max 1 rok wstecz')


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    update_date = models.DateTimeField(auto_now=True, validators=[validate_date])


class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_date = models.DateTimeField(auto_now_add= True, validators=[validate_date])
    user_agent = models.TextField(null=True, blank=True) # przechowa rodaj przeglądarki
    session_id = models.CharField(max_length=255, null=True, blank=True)  #  unikalne ID sesji do zapamietania logowania
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    failed_login_attempts = models.IntegerField(default=0)  #  ilosc błednych logowań
    cnt_modification = models.IntegerField(default=0) # ilość modyfikacji podczas zalogowania
    cnt_entries = models.IntegerField(default=0) # ilość wpisów podczas zalogowania
    cnt_deleted = models.IntegerField(default=0) # ilość skasowanych wpisów podczas zalogowania
    cnt_all_deleted = models.IntegerField(default=0) # ilość czyszczenia wszystkich wpisów podczas zalogowania


def __str__(self):
    return f'Użyt.: {self.user} Urodz.: {self.birthday} płec: {self.gender} akt.: {self.update_date} historia: {self.login_date}'
