from django.shortcuts import render
from .models import Pressure

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