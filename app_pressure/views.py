from django.shortcuts import render
from .models import Pressure

# Create your views here.
def all_pressures(request):
    found_pressures = Pressure.objects.all()
    context = {
        'pressures': found_pressures,
    }
    return render(request,'app_pressure/all_pressures.html', context)