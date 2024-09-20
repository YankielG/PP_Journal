from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from .models import Growth
from django.http import HttpResponseNotFound, HttpResponseForbidden
from .forms import Add_growth_Form
from django.db.models import Avg, Min, Max, Count

from django.core.paginator import Paginator

from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
def all_growths(request):
    logged_user = request.user
    filter_value = request.GET.get('search')

    if filter_value and len(filter_value) > 2:
        found_growths = Growth.objects.filter(owner=logged_user, comments__contains = filter_value)
    else:
        found_growths = Growth.objects.filter(owner=logged_user).order_by('-creation_date')

    page_num = request.GET.get('page', 1)
    pages = Paginator(found_growths, 3)

    pages_max = pages.num_pages
    pages_max_elements = pages.count
    page_results = pages.get_page(page_num)

    value_y = found_growths.values_list('growth', flat=True)
    chart_y = [float(y) for y in value_y]

    value_x = found_growths.values_list('creation_date', flat=True)
    chart_x = [x.strftime("%Y-%m-%d %H:%M") for x in value_x]

    context = {
        'filter_value': filter_value,
        'pages_max': pages_max,
        'pages_max_elements': pages_max_elements,
        'growths': page_results,
        'chart_x': chart_x,
        'chart_y': chart_y
    }
    return render(request,'app_growth/all_growths.html', context)

@login_required
def growth_details(request, id):
    logged_user = request.user
    found_growths = Growth.objects.filter(owner=logged_user)
    growth_statistical_data = found_growths.aggregate(Avg('growth'), Min('growth'), Max('growth'), Count('growth'))
    number = request.POST.get('number')
    found_growth = Growth.objects.get(pk=id)

    if not found_growth:
        return HttpResponseNotFound('Zasób nie został znaleziony')
    context = {
        'number': number,
        'growth': found_growth,
        'statistical_data': growth_statistical_data
    }
    return render(request,'app_growth/growth_details.html', context)

@login_required
def add_growth(request):
    logged_user = request.user
    if request.method == 'POST':
        growth = request.POST['growth']
        date = request.POST['date']
        comments = request.POST['comment']
        Growth.objects.create(growth=growth, creation_date=date, comments=comments, owner=logged_user)
        return redirect('all_growths_url')

    context = {
        'time_value': datetime.now().strftime("%Y-%m-%dT%H:%M"),
        'time_max': datetime.now().strftime("%Y-%m-%dT%H:%M"),
        'time_min': (datetime.now() - timedelta(weeks=52)).strftime("%Y-%m-%dT%H:%M")
    }
    return render(request, 'app_growth/add_growth.html', context)

@login_required
def edit_growth(request, id):
    logged_user = request.user
    found_growth = Growth.objects.get(pk=id)
    if request.method == 'POST':
        growth = request.POST['growth']
        date = request.POST['date']
        comments = request.POST['comment']
        found_growth.delete()
        Growth.objects.create(pk=id, growth=growth, creation_date=date, comments=comments, owner=logged_user)
        return redirect('all_growths_url')

    context = {
        'growth': found_growth,
        'time_value': found_growth.creation_date.strftime("%Y-%m-%dT%H:%M"),
        'time_max': datetime.now().strftime("%Y-%m-%dT%H:%M"),
        'time_min': (datetime.now() - timedelta(weeks=52)).strftime("%Y-%m-%dT%H:%M")
    }
    return render(request, 'app_growth/edit_growth.html', context)

@login_required
def delete_growth(request, id):
    logged_user = request.user
    found_growth = Growth.objects.get(pk=id)
    found_growth.delete()
    return redirect('all_growths_url')

@login_required
def delete_all_growth(request):
    logged_user = request.user
    found_growths = Growth.objects.filter(owner=logged_user)
    found_growths.delete()
    return redirect('all_growths_url')
