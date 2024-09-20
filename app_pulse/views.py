from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from .models import Pulse
from django.http import HttpResponseNotFound, HttpResponseForbidden
from .forms import Add_pulse_Form
from django.db.models import Avg, Min, Max, Count

from django.core.paginator import Paginator

from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
def all_pulses(request):
    logged_user = request.user
    filter_value = request.GET.get('search')

    if filter_value and len(filter_value) > 2:
        found_pulses = Pulse.objects.filter(owner=logged_user, comments__contains = filter_value)
    else:
        found_pulses = Pulse.objects.filter(owner=logged_user).order_by('-creation_date')

    page_num = request.GET.get('page', 1)
    pages = Paginator(found_pulses, 3)

    pages_max = pages.num_pages
    pages_max_elements = pages.count
    page_results = pages.get_page(page_num)

    value_y = found_pulses.values_list('pulse', flat=True)
    chart_y = [float(y) for y in value_y]

    value_x = found_pulses.values_list('creation_date', flat=True)
    chart_x = [x.strftime("%Y-%m-%d %H:%M") for x in value_x]

    context = {
        'filter_value': filter_value,
        'pages_max': pages_max,
        'pages_max_elements': pages_max_elements,
        'pulses': page_results,
        'chart_x': chart_x,
        'chart_y': chart_y
    }
    return render(request,'app_pulse/all_pulses.html', context)

@login_required
def pulse_details(request, id):
    logged_user = request.user
    found_pulses = Pulse.objects.filter(owner=logged_user)
    pulse_statistical_data = found_pulses.aggregate(Avg('pulse'), Min('pulse'), Max('pulse'), Count('pulse'))
    number = request.POST.get('number')
    found_pulse = Pulse.objects.get(pk=id)

    if not found_pulse:
        return HttpResponseNotFound('Zasób nie został znaleziony')
    context = {
        'number': number,
        'pulse': found_pulse,
        'statistical_data': pulse_statistical_data
    }
    return render(request,'app_pulse/pulse_details.html', context)

@login_required
def add_pulse(request):
    logged_user = request.user
    if request.method == 'POST':
        pulse = request.POST['pulse']
        date = request.POST['date']
        comments = request.POST['comment']
        Pulse.objects.create(pulse=pulse, creation_date=date, comments=comments, owner=logged_user)
        return redirect('all_pulses_url')

    context = {
        'time_value': datetime.now().strftime("%Y-%m-%dT%H:%M"),
        'time_max': datetime.now().strftime("%Y-%m-%dT%H:%M"),
        'time_min': (datetime.now() - timedelta(weeks=52)).strftime("%Y-%m-%dT%H:%M")
    }
    return render(request, 'app_pulse/add_pulse.html', context)

@login_required
def edit_pulse(request, id):
    logged_user = request.user
    found_pulse = Pulse.objects.get(pk=id)
    if request.method == 'POST':
        pulse = request.POST['pulse']
        date = request.POST['date']
        comments = request.POST['comment']
        found_pulse.delete()
        Pulse.objects.create(pk=id, pulse=pulse, creation_date=date, comments=comments, owner=logged_user)
        return redirect('all_pulses_url')

    context = {
        'pulse': found_pulse,
        'time_value': found_pulse.creation_date.strftime("%Y-%m-%dT%H:%M"),
        'time_max': datetime.now().strftime("%Y-%m-%dT%H:%M"),
        'time_min': (datetime.now() - timedelta(weeks=52)).strftime("%Y-%m-%dT%H:%M")
    }
    return render(request, 'app_pulse/edit_pulse.html', context)

@login_required
def delete_pulse(request, id):
    logged_user = request.user
    found_pulse = Pulse.objects.get(pk=id)
    found_pulse.delete()
    return redirect('all_pulses_url')

@login_required
def delete_all_pulse(request):
    logged_user = request.user
    found_pulses = Pulse.objects.filter(owner=logged_user)
    found_pulses.delete()
    return redirect('all_pulses_url')
