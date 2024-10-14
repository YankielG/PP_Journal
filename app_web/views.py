from datetime import datetime, timedelta
from functools import wraps
from lib2to3.fixes.fix_input import context

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound, HttpResponseForbidden, HttpResponseRedirect

from app_weight.models import Weight
from app_growth.models import Growth
from app_pressure.models import Pressure
from app_pulse.models import Pulse
from app_users.models import UserProfile, LoginHistory
from django.contrib.auth.models import User

# from .forms import Add_web_Form
from django.db.models import Avg, Min, Max, Count

from django.core.paginator import Paginator

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import update_session_auth_hash, get_user_model, authenticate, login, logout

from django.contrib import messages


@login_required
def info(request):
    logged_user = request.user
    context = {
        'time_value': datetime.now().strftime("%Y-%m-%dT%H:%M"),
        'message': ''
    }
    return render(request, 'app_web/info.html', context)


def error(request):
    context = {
        'time_value': datetime.now().strftime("%Y-%m-%d  %H:%M"),
        'message': ''
    }
    return render(request, '404.html', context)


@login_required
def home(request):
    logged_user = request.user
    last_login = logged_user.last_login
    date_joined = logged_user.date_joined
    cnt_visits = LoginHistory.objects.filter(user=logged_user).aggregate(login_count=Count('login_date'))

    user_profile = UserProfile.objects.get(user=logged_user)
    gender = user_profile.gender
    birthday = user_profile.birthday

    today = datetime.now()
    age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
    date_account = today.year - date_joined.year - ((today.month, today.day) < (date_joined.month, date_joined.day))

    found_growth = Growth.objects.filter(owner=logged_user)
    found_pressure = Pressure.objects.filter(owner=logged_user)
    found_pulse = Pulse.objects.filter(owner=logged_user)
    found_weight = Weight.objects.filter(owner=logged_user)

    total_entries = found_growth.count() + found_pressure.count() + found_pulse.count() + found_weight.count()

    if found_growth:
        last_growth = Growth.objects.latest("creation_date")
    else:
        last_growth = None
    if found_pressure:
        last_pressure = Pressure.objects.latest("creation_date")
    else:
        last_pressure = None
    if found_pulse:
        last_pulse = Pulse.objects.latest("creation_date")
    else:
        last_pulse = None
    if found_weight:
        last_weight = Weight.objects.latest('creation_date')
    else:
        last_weight = None

    if found_weight and found_growth:
        bmi_value = float(round(last_weight.weight / (last_growth.growth / 100 * last_growth.growth / 100), 2))
        value_chart = 50 - bmi_value
        chart = [bmi_value, value_chart]
        if gender == 'Mężczyzna':
            ppm_value = 66 + (13.7 * float(last_weight.weight)) + (5 * float(last_growth.growth)) - (6.8 * age)
        elif gender == 'Kobieta':
            ppm_value = 655 + (9.6 * float(last_weight.weight)) + (1.8 * float(last_growth.growth)) - (4.7 * age)
        else:
            ppm_value = 0
        ppm_comment = ""
    else:
        bmi_value = 0
        ppm_value = 0
        value_chart = 50 - bmi_value
        chart = [bmi_value, value_chart]
        if gender == 'Mężczyzna':
            ppm_comment = "Dokonaj wpisów wagi i wzrostu, PPM to: 66 + (13.7 * waga) + (5 * wzrost) - (6.8 * wiek)"
        elif gender == 'Kobieta':
            ppm_comment = "Dokonaj wpisów wagi i wzrostu, PPM to: 655 + (9.6 * waga) + (1.8 * wzrost) - (4.7 * wiek)"
        else:
            ppm_comment = "Brak pułci"

    bmi_rate = 'Brak Oceny'
    ppm_rate = 'Brak Oceny'
    bmi_color = '#CD853F'
    bmi_comment = 'Dokonaj wpisów wagi i wzrostu, BMI to: masa / wzrost * 2'

    if bmi_value < 5:
        pass
    elif bmi_value < 18.5:
        bmi_rate = 'Niskie'
        ppm_rate = 'Niskie BMI'
        bmi_color = '#0000FF'
        bmi_comment = 'Twoje BMI jest za niskie, jedź więcej. Skonsultuj sie z lekarzem.'
        ppm_comment = 'Jesz za mało kalorii, trzymaj się swojego poziomu. Skonsultuj sie z lekarzem.'
    elif bmi_value < 25:
        bmi_rate = 'W normie'
        ppm_rate = 'W normie BMI'
        bmi_color = '#32CD32'
        bmi_comment = 'Twoje BMI OK tak trzymaj.'
        ppm_comment = 'Jesz odpowiednią ilość kalorii, tak trzymaj.'
    elif bmi_value < 30:
        bmi_rate = 'Wysokie'
        ppm_rate = 'Wysokie BMI'
        bmi_color = '#FFA500'
        bmi_comment = 'Twoje BMI przekracza limit. Muszisz więcej ćwiczyć, aby poprawić sylwetkę'
        ppm_comment = 'Jesz za dużo kalorii, trzymaj się swojego poziomu'
    else:
        bmi_rate = 'Bardzo Wysokie'
        ppm_rate = 'Bardzo Wysokie BMI'
        bmi_color = '#FF0000'
        bmi_comment = 'Twoje BMI przekracza limit. Muszisz więcej ćwiczyć i stosować dietę. Skonsultuj sie z lekarzem.'
        ppm_comment = 'Jesz za dużo kalorii, trzymaj się swojego poziomu. Skonsultuj sie z lekarzem.'

    context = {
        'logged_user': logged_user,
        'date_account': date_account,
        'cnt_visits': cnt_visits,
        'total_entries': total_entries,
        'age': age,
        'chart': chart,
        'bmi_value': bmi_value,
        'ppm_value': ppm_value,
        'bmi_rate': bmi_rate,
        'ppm_rate': ppm_rate,
        'bmi_color': bmi_color,
        'bmi_comment': bmi_comment,
        'ppm_comment': ppm_comment,
        'last_growth': last_growth,
        'last_weight': last_weight,
        'last_pressure': last_pressure,
        'last_pulse': last_pulse,

    }
    return render(request, 'app_web//home.html', context)
