from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from .models import Growth
from django.http import HttpResponseNotFound, HttpResponseForbidden
from .forms import Add_growth_Form
from django.db.models import Avg, Min, Max, Count

# Create your views here.
def all_growths(request):
    found_growths = Growth.objects.all()

    value_y = Growth.objects.values_list('growth', flat=True)
    chart_y = [float(y) for y in value_y]

    value_x = found_growths.values_list('date', flat=True)
    chart_x = [x.strftime("%Y-%m-%d %H:%M") for x in value_x]

    context = {
        'growths': found_growths,
        'chart_x': chart_x,
        'chart_y': chart_y
    }
    return render(request,'app_growth/all_growths.html', context)

def growth_details(request, id):
    found_growths = Growth.objects.all()
    growth_statistical_data = found_growths.aggregate(Avg('growth'), Min('growth'), Max('growth'), Count('growth'))

    found_growth = Growth.objects.get(pk=id)

    if not found_growth:
        return HttpResponseNotFound('Zasób nie został znaleziony')
    context = {
        'growth': found_growth,
        'statistical_data': growth_statistical_data
    }
    return render(request,'app_growth/growth_details.html', context)

def add_growth(request):
    if request.method == 'POST':
        growth = request.POST['growth']
        date = request.POST['date']
        comments = request.POST['comment']
        Growth.objects.create(growth=growth, date=date, comments=comments)
        return redirect('all_growths_url')

    context = {
        'time_value': datetime.now().strftime("%Y-%m-%dT%H:%M"),
        'time_max': datetime.now().strftime("%Y-%m-%dT%H:%M"),
        'time_min': (datetime.now() - timedelta(weeks=52)).strftime("%Y-%m-%dT%H:%M")
    }
    return render(request, 'app_growth/add_growth.html', context)

def edit_growth(request, id):
    found_growth = Growth.objects.get(pk=id)
    if request.method == 'POST':
        growth = request.POST['growth']
        date = request.POST['date']
        comments = request.POST['comment']
        found_growth.delete()
        Growth.objects.create(pk=id, growth=growth, date=date, comments=comments)
        return redirect('all_growths_url')

    context = {
        'growth': found_growth,
        'time_value': found_growth.date.strftime("%Y-%m-%dT%H:%M"),
        'time_max': datetime.now().strftime("%Y-%m-%dT%H:%M"),
        'time_min': (datetime.now() - timedelta(weeks=52)).strftime("%Y-%m-%dT%H:%M")
    }
    return render(request, 'app_growth/edit_growth.html',context)

def delete_growth(request, id):
    found_growth = Growth.objects.get(pk=id)
    found_growth.delete()
    return redirect('all_growths_url')

def delete_all_growth(request):
    found_growths = Growth.objects.all()
    found_growths.delete()
    return redirect('all_growths_url')

