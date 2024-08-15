from datetime import datetime

from django.shortcuts import render, redirect
from .models import Weight
from django.http import HttpResponseNotFound, HttpResponseForbidden
from .forms import Add_weight_Form
from django.db.models import Avg, Min, Max, Count

# Create your views here.
def all_weights(request):
    found_weights = Weight.objects.all()
    context = {
        'weights': found_weights,
        'chart_x': [1,2,3,4,5],
        'chart_y': [50,55,60,65,70]
    }
    return render(request,'app_weight/all_weights.html', context)

def weight_details(request, id):
    found_weights = Weight.objects.all()
    weight_statistical_data = found_weights.aggregate(Avg('weight'), Min('weight'), Max('weight'), Count('weight'))

    found_weight = Weight.objects.get(pk=id)

    if not found_weight:
        return HttpResponseNotFound('Zasób nie został znaleziony')
    context = {
        'weight': found_weight,
        'statistical_data': weight_statistical_data
    }
    return render(request,'app_weight/weight_details.html', context)

def add_weight(request):

    if request.method == 'POST':
        weight = request.POST['weight']
        date = request.POST['date']
        comments = request.POST['comment']
        object = Weight(weight=weight, date=date, comments=comments)
        object.save()
        return redirect('all_weights_url')

    context = {
        'time_now': datetime.now().strftime("%Y-%m-%dT%H:%M")
    }
    print(context)
    return render(request, 'app_weight/add_weight.html',context)

def delete_weight(request, id):
    found_weight = Weight.objects.get(pk=id)
    found_weight.delete()
    return redirect('all_weights_url')

def delete_all_weight(request):
    found_weights = Weight.objects.all()
    found_weights.delete()
    return redirect('all_weights_url')

def edit_weight(request, id):
    return render(request, 'app_weight/edit_weight.html')


def info(request):
    return  render(request,'app_weight/info.html')


def error(request):
    return  render(request,'app_weight/error.html')


def home(request):
    return  render(request,'app_weight/home.html')
