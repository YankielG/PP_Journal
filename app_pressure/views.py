from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from .models import Pressure
from django.http import HttpResponseNotFound, HttpResponseForbidden
from .forms import Add_pressure_Form
from django.db.models import Avg, Min, Max, Count

# Create your views here.
def all_pressures(request):
    found_pressures = Pressure.objects.all()
    context = {
        'pressures': found_pressures,
        'chart_x': [1, 2, 3, 4, 5],
        'chart_y1': [45, 55, 70, 61, 78], #ciśnienie skurczowe
        'chart_y2': [55, 75, 58, 99, 88], #ciśnienei rozkurczowe
        'chart_y3': [50, 53, 68, 77, 85]  #tetno
    }
    return render(request,'app_pressure/all_pressures.html', context)

def pressure_details(request, id):
    found_pressures = Pressure.objects.all()
    shrink_statistical_data = found_pressures.aggregate(Avg('shrink'), Min('shrink'), Max('shrink'), Count('shrink'))
    diastole_statistical_data = found_pressures.aggregate(Avg('diastole'), Min('diastole'), Max('diastole'), Count('diastole'))
    pulse_statistical_data = found_pressures.aggregate(Avg('pulse'), Min('pulse'), Max('pulse'), Count('pulse'))

    found_pressure = Pressure.objects.get(pk=id)

    if not found_pressure:
        return HttpResponseNotFound('Zasób nie został znaleziony')
    context = {
        'pressure': found_pressure,
        'shrink_statistical_data': shrink_statistical_data,
        'diastole_statistical_data': diastole_statistical_data,
        'pulse_statistical_data': pulse_statistical_data
    }
    return render(request,'app_pressure/pressure_details.html', context)

def add_pressure(request):
    if request.method == 'POST':
        shrink = request.POST['shrink']
        diastole = request.POST['diastole']
        pulse = request.POST['pulse']
        date = request.POST['date']
        comments = request.POST['comment']
        Pressure.objects.create(shrink=shrink, diastole=diastole, pulse=pulse, date=date, comments=comments)
        return redirect('all_pressures_url')

    context = {
        'time_value': datetime.now().strftime("%Y-%m-%dT%H:%M"),
        'time_max': datetime.now().strftime("%Y-%m-%dT%H:%M"),
        'time_min': (datetime.now() - timedelta(weeks=52)).strftime("%Y-%m-%dT%H:%M")
    }
    return render(request, 'app_pressure/add_pressure.html', context)

def edit_pressure(request, id):
    found_pressure = Pressure.objects.get(pk=id)
    if request.method == 'POST':
        shrink = request.POST['shrink']
        diastole = request.POST['diastole']
        pulse = request.POST['pulse']
        date = request.POST['date']
        comments = request.POST['comment']
        found_pressure.delete()
        Pressure.objects.create(pk=id, shrink=shrink, diastole=diastole, pulse=pulse, date=date, comments=comments)
        return redirect('all_pressures_url')

    context = {
        'pressure': found_pressure,
        'time_value': found_pressure.date.strftime("%Y-%m-%dT%H:%M"),
        'time_max': datetime.now().strftime("%Y-%m-%dT%H:%M"),
        'time_min': (datetime.now() - timedelta(weeks=52)).strftime("%Y-%m-%dT%H:%M")
    }
    return render(request, 'app_pressure/edit_pressure.html',context)

def delete_pressure(request, id):
    found_pressure = Pressure.objects.get(pk=id)
    found_pressure.delete()
    return redirect('all_pressures_url')

def delete_all_pressure(request):
    found_pressures = Pressure.objects.all()
    found_pressures.delete()
    return redirect('all_pressures_url')

