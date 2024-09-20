from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from .models import Weight
from django.http import HttpResponseNotFound, HttpResponseForbidden
from .forms import Add_weight_Form
from django.db.models import Avg, Min, Max, Count

from django.core.paginator import Paginator

from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
def all_weights(request):
    logged_user = request.user
    filter_value = request.GET.get('search')

    if filter_value and len(filter_value) > 2:
        found_weights = Weight.objects.filter(owner=logged_user, comments__contains = filter_value)
    else:
        found_weights = Weight.objects.filter(owner=logged_user).order_by('-creation_date')

    page_num = request.GET.get('page', 1)
    pages = Paginator(found_weights, 3)

    pages_max = pages.num_pages
    pages_max_elements = pages.count
    page_results = pages.get_page(page_num)

    value_y = found_weights.values_list('weight', flat=True)
    chart_y = [float(y) for y in value_y]

    value_x = found_weights.values_list('creation_date', flat=True)
    chart_x = [x.strftime("%Y-%m-%d %H:%M") for x in value_x]

    context = {
        'filter_value' : filter_value,
        'pages_max': pages_max,
        'pages_max_elements': pages_max_elements,
        'weights': page_results,
        'chart_x': chart_x,
        'chart_y': chart_y
    }
    return render(request,'app_weight/all_weights.html', context)

@login_required
def weight_details(request, id):
    logged_user = request.user
    found_weights = Weight.objects.filter(owner=logged_user)
    weight_statistical_data = found_weights.aggregate(Avg('weight'), Min('weight'), Max('weight'), Count('weight'))
    number = request.POST.get('number')
    found_weight = Weight.objects.get(pk=id)

    if not found_weight:
        return HttpResponseNotFound('Zasób nie został znaleziony')
    context = {
        'number': number,
        'weight': found_weight,
        'statistical_data': weight_statistical_data
    }
    return render(request,'app_weight/weight_details.html', context)

@login_required
def add_weight(request):
    logged_user = request.user
    if request.method == 'POST':
        weight = request.POST['weight']
        date = request.POST['date']
        comments = request.POST['comment']
        object = Weight(weight=weight, creation_date=date, comments=comments, owner=logged_user)
        object.save()
        return redirect('all_weights_url')

    context = {
        'time_value': datetime.now().strftime("%Y-%m-%dT%H:%M"),
        'time_max': datetime.now().strftime("%Y-%m-%dT%H:%M"),
        'time_min': (datetime.now() - timedelta(weeks=52)).strftime("%Y-%m-%dT%H:%M")
    }
    return render(request, 'app_weight/add_weight.html',context)

@login_required
def edit_weight(request, id):
    logged_user = request.user
    found_weight = Weight.objects.get(pk=id)
    if request.method == 'POST':
        # found_weight.weight = request.POST['weight']
        # found_weight.creation_date = request.POST['date']
        # found_weight.comments = request.POST['comment']
        # found_weight.save()
        weight = request.POST['weight']
        date = request.POST['date']
        comments = request.POST['comment']
        found_weight.delete()
        Weight.objects.create(pk=id, weight=weight, creation_date=date, comments=comments, owner=logged_user)
        return redirect('all_weights_url')

    context = {
        'weight': found_weight,
        'time_value': found_weight.creation_date.strftime("%Y-%m-%dT%H:%M"),
        'time_max': datetime.now().strftime("%Y-%m-%dT%H:%M"),
        'time_min': (datetime.now() - timedelta(weeks=52)).strftime("%Y-%m-%dT%H:%M")
    }
    return render(request, 'app_weight/edit_weight.html', context)

@login_required
def delete_weight(request, id):
    logged_user = request.user
    found_weight = Weight.objects.get(pk=id)
    found_weight.delete()
    return redirect('all_weights_url')

@login_required
def delete_all_weight(request):
    logged_user = request.user
    found_weights = Weight.objects.filter(owner=logged_user)
    found_weights.delete()
    return redirect('all_weights_url')
