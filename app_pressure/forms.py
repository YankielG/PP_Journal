from django import forms
from django.core.validators import MinValueValidator, RegexValidator, MaxValueValidator, MinLengthValidator
from django.forms.utils import ErrorList
from . import models

class Add_pressure_Form(forms.Form):
    shrink = forms.DecimalField(label='Ciśnienie skurczowe', max_digits=3, decimal_places=1)
    diastole = forms.DecimalField(label='Ciśnienie rozkurczowe', max_digits=3, decimal_places=1)
    pulse = forms.DecimalField(label='Tętno', max_digits=3, decimal_places=1)
    date = forms.DateTimeField(label='Data'),
    comments = forms.CharField(label='Uwagi', max_length=255)
