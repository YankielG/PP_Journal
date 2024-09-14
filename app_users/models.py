from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta


def validate_date(value):
    if value.date() < datetime.now().date() - timedelta(weeks=10):
        raise ValidationError(f'{value} nie jest datą max 1 rok wstecz')


# Create your models here.
class Users(models.Model):
    user = models.CharField(max_length=20)
    date = models.DateTimeField(validators=[validate_date])
    comments = models.CharField(max_length=255, validators=[MaxLengthValidator(150)])

    def __str__(self):
        return f'Użytkownik: {self.weight} Data: {self.date} Uwagi: {self.comments}'