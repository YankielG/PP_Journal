from django.shortcuts import render
from .models import Growth

# Create your views here.
def all_growths(request):
    found_growths = Growth.objects.all()
    context = {
        'growths': found_growths,
        'chart_x': [1, 2, 3, 4, 5],
        'chart_y': [50, 55, 60, 65, 70]
    }
    return render(request,'app_growth/all_growths.html', context)