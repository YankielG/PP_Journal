from django.shortcuts import render
from .models import Weight

# Create your views here.
def all_weights(request):
    found_weights = Weight.objects.all()
    context = {
        'weights': found_weights,
    }
    return render(request,'app_weight/all_weights.html', context)