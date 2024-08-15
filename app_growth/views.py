from django.shortcuts import render, redirect
from .models import Growth
from django.http import HttpResponseNotFound
from django.db.models import Avg, Min, Max, Count

# Create your views here.
def all_growths(request):
    found_growths = Growth.objects.all()
    print(found_growths)
    context = {
        'growths': found_growths,
        'chart_x': [1,2,3,4,5],
        'chart_y': [50,55,60,65,70]
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
    return render(request, 'app_growth/add_growth.html')

def delete_growth(request, id):
    found_growth = Growth.objects.get(pk=id)
    found_growth.delete()
    return redirect('all_growths_url')

def delete_all_growth(request):
    found_growths = Growth.objects.all()
    found_growths.delete()
    return redirect('all_growths_url')

def edit_growth(request, id):
    return render(request, 'app_growth/edit_growth.html')