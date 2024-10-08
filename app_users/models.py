from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from django.contrib.auth.models import User
#
#
def validate_date(value):
    if value.date() < datetime.now().date() - timedelta(weeks=5200):
        raise ValidationError(f'{value} nie jest datą max 1 rok wstecz')

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(validators=[validate_date])
    gender = models.CharField(max_length=10, choices=(('M', 'Male'), ('F', 'Female')), default='M')
    update_date = models.DateTimeField(auto_now=True, validators=[validate_date])



class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_date = models.DateTimeField(auto_now_add= True, validators=[validate_date])

    # ip_address = models.GenericIPAddressField(null=True, blank=True)
    # user_agent = models.TextField(null=True, blank=True) # przechowa rodaj przeglądarki
    # login_status = models.BooleanField(default=False)  #  przechowa status zalogowania udany błędny
    # failed_login_attempts = models.IntegerField(default=0)  #  ilosc błednych logowań
    # session_id = models.CharField(max_length=255, null=True, blank=True)  #  unikalne ID sesji do zapamietania logowania


def __str__(self):
    return f'Użyt.: {self.user} Urodz.: {self.birthday} płec: {self.gender} akt.: {self.update_date} historia: {self.login_date}'

'''
z dokumentacji wynika ze dostęp jest
user = User.objects.get(username='example')
phone_number = user.userprofile.phone_number

'''