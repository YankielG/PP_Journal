from django.shortcuts import render
from .models import Weight
from django.http import HttpResponseNotFound
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

def info(request):
    return  render(request,'app_weight/info.html')


def error(request):
    return  render(request,'app_weight/error.html')


def home(request):
    return  render(request,'app_weight/home.html')
