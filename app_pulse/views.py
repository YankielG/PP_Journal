from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from .models import Pulse
from django.http import HttpResponseNotFound, HttpResponseForbidden
from .forms import Add_pulse_Form
from django.db.models import Avg, Min, Max, Count

# Create your views here.
def all_pulses(request):
    found_pulses = Pulse.objects.all()
    context = {
        'pulses': found_pulses,
        'chart_x': [1, 2, 3, 4, 5],
        'chart_y': [50, 55, 60, 65, 70]
    }
    return render(request,'app_pulse/all_pulses.html', context)

def pulse_details(request, id):
    found_pulses = Pulse.objects.all()
    pulse_statistical_data = found_pulses.aggregate(Avg('pulse'), Min('pulse'), Max('pulse'), Count('pulse'))

    found_pulse = Pulse.objects.get(pk=id)

    if not found_pulse:
        return HttpResponseNotFound('Zasób nie został znaleziony')
    context = {
        'pulse': found_pulse,
        'statistical_data': pulse_statistical_data
    }
    return render(request,'app_pulse/pulse_details.html', context)

def add_pulse(request):
    if request.method == 'POST':
        pulse = request.POST['pulse']
        date = request.POST['date']
        comments = request.POST['comment']
        Pulse.objects.create(pulse=pulse, date=date, comments=comments)
        return redirect('all_pulses_url')

    context = {
        'time_value': datetime.now().strftime("%Y-%m-%dT%H:%M"),
        'time_max': datetime.now().strftime("%Y-%m-%dT%H:%M"),
        'time_min': (datetime.now() - timedelta(weeks=52)).strftime("%Y-%m-%dT%H:%M")
    }
    return render(request, 'app_pulse/add_pulse.html', context)

def edit_pulse(request, id):
    found_pulse = Pulse.objects.get(pk=id)
    if request.method == 'POST':
        pulse = request.POST['pulse']
        date = request.POST['date']
        comments = request.POST['comment']
        found_pulse.delete()
        Pulse.objects.create(pk=id, pulse=pulse, date=date, comments=comments)
        return redirect('all_pulses_url')

    context = {
        'pulse': found_pulse,
        'time_value': found_pulse.date.strftime("%Y-%m-%dT%H:%M"),
        'time_max': datetime.now().strftime("%Y-%m-%dT%H:%M"),
        'time_min': (datetime.now() - timedelta(weeks=52)).strftime("%Y-%m-%dT%H:%M")
    }
    return render(request, 'app_pulse/edit_pulse.html', context)

def delete_pulse(request, id):
    found_pulse = Pulse.objects.get(pk=id)
    found_pulse.delete()
    return redirect('all_pulses_url')

def delete_all_pulse(request):
    found_pulses = Pulse.objects.all()
    found_pulses.delete()
    return redirect('all_pulses_url')

