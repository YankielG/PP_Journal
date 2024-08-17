from django import forms
from django.core.validators import MinValueValidator, RegexValidator, MaxValueValidator, MinLengthValidator
from django.forms.utils import ErrorList
from . import models

class Add_weight_Form(forms.Form):
    weight = forms.DecimalField(label='Waga', max_digits=3, decimal_places=1),
    date = forms.DateTimeField(label='Data'),
    comments = forms.CharField(label='Uwagi', max_length=255)


