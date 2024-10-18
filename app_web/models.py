# from django.db import models
# from django.core.validators import MinValueValidator, MaxValueValidator, MaxLengthValidator
# from django.core.exceptions import ValidationError
# from datetime import datetime, timedelta
# from django.contrib.auth.models import User
#
# def validate_date(value):
#     if value.date() < datetime.now().date() - timedelta(weeks=10):
#         raise ValidationError(f'{value} nie jest datą max 1 rok wstecz')
#
#
# # Create your models here.
# class Web(models.Model):
#     version = models.DecimalField(max_digits=5, decimal_places=1,
#                                  validators=[MinValueValidator(0), MaxValueValidator(20)])
#     creation_date = models.DateTimeField(auto_now_add=True, validators=[validate_date])
#     update_date = models.DateTimeField(auto_now=True, validators=[validate_date])
#     cnt_modification = models.IntegerField(default=0)  # ilość modyfikacji wpisu
#     comments = models.CharField(max_length=255, validators=[MaxLengthValidator(150)])
#     owner = models.ForeignKey(User, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return f'wesja: {self.version} Data wpisu: {self.creation_date} Data akt.: {self.update_date} Uwagi: {self.comments} właściciel: {self.owner}'

