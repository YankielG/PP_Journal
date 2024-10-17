from datetime import datetime, timedelta
from functools import wraps

from django.shortcuts import render, redirect, get_object_or_404
from django.template.context_processors import request

from .models import Pressure
from app_users.models import LoginHistory
from django.http import HttpResponseNotFound, HttpResponseForbidden, HttpResponseRedirect

from .forms import Add_pressure_Form
from django.db.models import Avg, Min, Max, Count

from django.core.paginator import Paginator

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test


def check_owner(private_view):

    # @wraps(private_view)
    def owner_view(request, id, *args, **kwargs):
        logged_user = request.user
        record_owner = Pressure.objects.get(pk=id).owner
        if logged_user == record_owner:
            return private_view(request, id, *args, **kwargs)
        else:
            # context = {
            #     'title': '403',
            #     'time_value': datetime.now().strftime("%Y-%m-%d  %H:%M"),
            #     'message': 'Nie masz dostępu do tego zasobu'
            # }
            # return render(request, '404.html', context)
            return HttpResponseRedirect('/')
            # return HttpResponseNotFound('Zasób nie został znaleziony')
            # return HttpResponseForbidden('Nie masz dostępu do tego wpisu')

    return owner_view


@login_required
def all_pressures(request):
    logged_user = request.user
    filter_value = request.GET.get('search')

    if filter_value and len(filter_value) > 2:
        found_pressures = Pressure.objects.filter(owner=logged_user, comments__contains = filter_value)
    else:
        found_pressures = Pressure.objects.filter(owner=logged_user).order_by('-creation_date')

    page_num = request.GET.get('page', 1)
    pages = Paginator(found_pressures, 3)

    pages_max = pages.num_pages
    pages_max_elements = pages.count
    page_results = pages.get_page(page_num)

    value_y1 = found_pressures.values_list('shrink', flat=True)
    chart_y1 = [float(y) for y in value_y1]

    value_y2 = found_pressures.values_list('diastole', flat=True)
    chart_y2 = [float(y) for y in value_y2]

    value_y3 = found_pressures.values_list('pulse', flat=True)
    chart_y3 = [float(y) for y in value_y3]

    value_x = found_pressures.values_list('creation_date', flat=True)
    chart_x = [x.strftime("%Y-%m-%d %H:%M") for x in value_x]

    context = {
        'filter_value': filter_value,
        'pages_max': pages_max,
        'pages_max_elements': pages_max_elements,
        'pressures': page_results,
        'chart_x':  chart_x,
        'chart_y1': chart_y1, #ciśnienie skurczowe
        'chart_y2': chart_y2, #ciśnienei rozkurczowe
        'chart_y3': chart_y3  #tetno
    }
    return render(request,'app_pressure/all_pressures.html', context)

@login_required
@check_owner
def pressure_details(request, id):
    logged_user = request.user
    found_pressures = Pressure.objects.filter(owner=logged_user)
    shrink_statistical_data = found_pressures.aggregate(Avg('shrink'), Min('shrink'), Max('shrink'), Count('shrink'))
    diastole_statistical_data = found_pressures.aggregate(Avg('diastole'), Min('diastole'), Max('diastole'), Count('diastole'))
    pulse_statistical_data = found_pressures.aggregate(Avg('pulse'), Min('pulse'), Max('pulse'), Count('pulse'))

    number = request.POST.get('number')
    found_pressure = Pressure.objects.get(pk=id)

    current_element_index = 0
    for i,g in enumerate(found_pressures):
        if g.id == found_pressure.id:
            current_element_index = i
            break

    first_detail = current_element_index == 0
    last_detail = current_element_index == len(found_pressures) - 1

    prev_view = found_pressures[current_element_index - 1] if not first_detail else None
    next_view = found_pressures[current_element_index + 1] if not last_detail else None
    first_view = found_pressures[0] if not first_detail else None
    last_view = found_pressures[len(found_pressures) - 1] if not last_detail else None
    all_element_index = len(found_pressures)
    number = current_element_index + 1

    if not found_pressure:
        return HttpResponseNotFound('Zasób nie został znaleziony')
    context = {
        'number': number,
        'pressure': found_pressure,
        'shrink_statistical_data': shrink_statistical_data,
        'diastole_statistical_data': diastole_statistical_data,
        'pulse_statistical_data': pulse_statistical_data,
        'prev_view': prev_view,
        'next_view': next_view,
        'first_view': first_view,
        'last_view': last_view,
        'current_element_index': current_element_index + 1,
        'all_element_index': all_element_index,
    }
    return render(request,'app_pressure/pressure_details.html', context)

@login_required
def add_pressure(request):
    logged_user = request.user
    if request.method == 'POST':
        shrink = request.POST['shrink']
        diastole = request.POST['diastole']
        pulse = request.POST['pulse']
        date = request.POST['date']
        comments = request.POST['comment']
        Pressure.objects.create(shrink=shrink, diastole=diastole, pulse=pulse, creation_date=date, comments=comments, owner=logged_user)

        login_history = LoginHistory.objects.filter(user=logged_user).last()
        login_history.cnt_entries +=1
        login_history.save()
        return redirect('all_pressures_url')

    context = {
        'time_value': datetime.now().strftime("%Y-%m-%dT%H:%M"),
        'time_max': datetime.now().strftime("%Y-%m-%dT%H:%M"),
        'time_min': (datetime.now() - timedelta(weeks=52)).strftime("%Y-%m-%dT%H:%M")
    }
    return render(request, 'app_pressure/add_pressure.html', context)

@login_required
@check_owner
def edit_pressure(request, id):
    logged_user = request.user
    found_pressure = Pressure.objects.get(pk=id)
    if request.method == 'POST':
        shrink = request.POST['shrink']
        diastole = request.POST['diastole']
        pulse = request.POST['pulse']
        date = request.POST['date']
        comments = request.POST['comment']
        found_pressure.delete()
        Pressure.objects.create(pk=id, shrink=shrink, diastole=diastole, pulse=pulse, creation_date=date, comments=comments, owner=logged_user)

        login_history = LoginHistory.objects.filter(user=logged_user).last()
        login_history.cnt_modification +=1
        login_history.save()
        return redirect('all_pressures_url')

    context = {
        'pressure': found_pressure,
        'time_value': found_pressure.creation_date.strftime("%Y-%m-%dT%H:%M"),
        'time_max': datetime.now().strftime("%Y-%m-%dT%H:%M"),
        'time_min': (datetime.now() - timedelta(weeks=52)).strftime("%Y-%m-%dT%H:%M")
    }
    return render(request, 'app_pressure/edit_pressure.html',context)

@login_required
@check_owner
def delete_pressure(request, id):
    logged_user = request.user
    found_pressure = Pressure.objects.get(pk=id)
    found_pressure.delete()

    login_history = LoginHistory.objects.filter(user=logged_user).last()
    login_history.cnt_deleted += 1
    login_history.save()
    return redirect('all_pressures_url')

@login_required
def delete_all_pressure(request):
    logged_user = request.user
    found_pressures = Pressure.objects.filter(owner=logged_user)
    found_pressures.delete()

    login_history = LoginHistory.objects.filter(user=logged_user).last()
    login_history.cnt_all_deleted += 1
    login_history.save()
    return redirect('all_pressures_url')
