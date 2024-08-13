from django.shortcuts import render
from .models import Pulse

# Create your views here.
def all_pulses(request):
    found_pulses = Pulse.objects.all()
    context = {
        'pulses': found_pulses,
        'chart_x': [1, 2, 3, 4, 5],
        'chart_y': [50, 55, 60, 65, 70]
    }
    return render(request,'app_pulse/all_pulses.html', context)