from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from app_weight.models import Weight
from app_growth.models import Growth
from django.http import HttpResponseNotFound, HttpResponseForbidden
# from .forms import Add_web_Form
from django.db.models import Avg, Min, Max, Count

from django.core.paginator import Paginator

# Create your views here.
def info(request):
    return  render(request, 'app_web/info.html')


def error(request):
    return  render(request, '404.html')


def home(request):
    found_weights = Weight.objects.all()
    found_growth = Growth.objects.all()

    if found_weights and found_growth:
        last_weight = Weight.objects.latest('date')
        last_growth = Growth.objects.latest("date")
        bmi_value = float(round(last_weight.weight / (last_growth.growth/100 * last_growth.growth/100), 2))
        value_chart = 50 - bmi_value
        chart = [bmi_value, value_chart]
    else:
        bmi_value = 0
        value_chart = 50 - bmi_value
        chart = [bmi_value, value_chart]

    bmi_rate = 'Brak Oceny'
    bmi_color = '#CD853F'
    bmi_comment = 'Dokonaj wpisów wagi i wzrostu, BMI to: masa / wzrost * 2'
    if bmi_value < 5:
        pass
    elif bmi_value < 18.5 :
        bmi_rate = 'Niskie'
        bmi_color = '#0000FF'
        bmi_comment = 'Twoje BMI jest za niskie, jedź więcej. Skonsultuj sie z lekarzem.'
    elif bmi_value < 25:
        bmi_rate = 'W normie'
        bmi_color = '#32CD32'
        bmi_comment = 'Twoje BMI OK tak trzymaj.'
    elif bmi_value < 30:
        bmi_rate = 'Wysokie'
        bmi_color = '#FFA500'
        bmi_comment = 'Twoje BMI przekracza limit. Muszisz więcej ćwiczyć, aby poprawić sylwetkę'
    else:
        bmi_rate = 'Bardzo Wysokie'
        bmi_color = '#FF0000'
        bmi_comment = 'Twoje BMI przekracza limit. Muszisz więcej ćwiczyć i stosować dietę. Skonsultuj sie z lekarzem.'


    context = {
        'chart': chart,
        'bmi_value': bmi_value,
        'bmi_rate': bmi_rate,
        'bmi_color': bmi_color,
        'bmi_comment': bmi_comment
    }
    return  render(request, 'app_web//home.html', context)
