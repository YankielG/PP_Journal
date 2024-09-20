# from django import forms
# from django.core.validators import MinValueValidator, RegexValidator, MaxValueValidator, MinLengthValidator
# from django.forms.utils import ErrorList
# from django.core.exceptions import ValidationError
# from . import models
# from datetime import datetime, timedelta
# from django.contrib.auth.models import User
# from django.contrib.auth.decorators import login_required, user_passes_test

#
# def validate_date(value):
#     if value.date() < datetime.now().date() - timedelta(weeks=10):
#         raise ValidationError(f'{value} nie jest datą max 1 rok wstecz')
#
# class Add_web_Form(forms.Form):
#     version = forms.DecimalField(label='version', max_digits=5, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(20)]),
#     creation_date = forms.DateTimeField(label='Data wpisu', validators=[validate_date], widget=forms.DateTimeInput(attrs={'class': 'datepicker', 'type': datetime}), initial=datetime.now().strftime("%Y-%m-%dT%H:%M")),
#     update_date = forms.DateTimeField(label='Data aktualizacji', validators=[validate_date], widget=forms.DateTimeInput(attrs={'class': 'datepicker', 'type': datetime}), initial=datetime.now().strftime("%Y-%m-%dT%H:%M")),
#     comments = forms.CharField(label='Uwagi', max_length=255, validators=[MinLengthValidator(2)], widget=forms.Textarea(attrs={'class': 'form-control', 'maxlength': 150, 'rows': 5, })),
#     owner = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput(), required=False)

#
#
# def __init__(self, *args, **kwargs):
#     super(Add_web_Form, self).__init__(*args, **kwargs)
#     for visible_field in self.visible_fields():
#         visible_field.field.widget.attrs['class'] = 'uk-input uk-margin-small-bottom'
