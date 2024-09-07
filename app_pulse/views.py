from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from .models import Pulse
from django.http import HttpResponseNotFound, HttpResponseForbidden
from .forms import Add_pulse_Form
from django.db.models import Avg, Min, Max, Count

from django.core.paginator import Paginator

# Create your views here.
def all_pulses(request):
    filter_value = request.GET.get('search')

    if filter_value and len(filter_value) > 2:
        found_pulses = Pulse.objects.filter(comments__contains = filter_value)
    else:
        found_pulses = Pulse.objects.all().order_by('date')

    page_num = request.GET.get('page', 1)
    pages = Paginator(found_pulses, 3)

    pages_max = pages.num_pages
    pages_max_elements = pages.count
    page_results = pages.get_page(page_num)

    value_y = Pulse.objects.values_list('pulse', flat=True)
    chart_y = [float(y) for y in value_y]

    value_x = found_pulses.values_list('date', flat=True)
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

def pulse_details(request, id):
    found_pulses = Pulse.objects.all()
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

