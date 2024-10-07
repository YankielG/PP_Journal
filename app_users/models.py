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


class LoginHistory(models.Model):
    login_date = models.DateTimeField(auto_now=True, validators=[validate_date])


class UsersProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    update_date = models.DateTimeField(auto_now=True, validators=[validate_date])
    birthday = models.DateField(validators=[validate_date])
    gender = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female')), default='M')
    history = models.ForeignKey(LoginHistory, on_delete=models.CASCADE)


    def __str__(self):
        return f'Użyt.: {self.user} Urodz.: {self.birthday} płec: {self.gender} akt.: {self.update_date} historia: {self.history}'