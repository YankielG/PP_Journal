from django import forms
from django.core.validators import MinValueValidator, RegexValidator, MaxValueValidator, MinLengthValidator
from django.forms.utils import ErrorList
from . import models

class Add_growth_Form(forms.Form):
    growth = forms.DecimalField(label='Wzrost', max_digits=5, decimal_places=1),
    date = forms.DateTimeField(label='Data'),
    comments = forms.CharField(label='Uwagi', max_length=255)
