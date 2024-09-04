from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta


def validate_date(value):
    if value.date() < datetime.now().date() - timedelta(weeks=10):
        raise ValidationError(f'{value} nie jest datą max 1 rok wstecz')


# Create your models here.
class Pulse(models.Model):
    pulse = models.DecimalField(max_digits=5, decimal_places=1,
                                validators=[MinValueValidator(40), MaxValueValidator(150)])
    date = models.DateTimeField(validators=[validate_date])
    comments = models.CharField(max_length=255, validators=[MaxLengthValidator(255)])

    def __str__(self):
        return f'Tetno: {self.pulse} Data: {self.date} Uwagi: {self.comments}'
