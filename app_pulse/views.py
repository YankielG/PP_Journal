from django.shortcuts import render
from .models import Pulse

# Create your views here.
def all_pulses(request):
    found_pulses = Pulse.objects.all()
    context = {
        'pulses': found_pulses,
    }
    return render(request,'app_pulse/all_pulses.html', context)