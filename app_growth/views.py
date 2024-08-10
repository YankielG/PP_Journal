from django.shortcuts import render
from .models import Growth

# Create your views here.
def all_growths(request):
    found_growths = Growth.objects.all()
    context = {
        'growths': found_growths,
    }
    return render(request,'app_growth/all_growths.html', context)