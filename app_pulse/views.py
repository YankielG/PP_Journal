from datetime import datetime, timedelta
from functools import wraps

from django.shortcuts import render, redirect, get_object_or_404
from django.template.context_processors import request

from .models import Pulse
from app_users.models import LoginHistory
from django.http import HttpResponseNotFound, HttpResponseForbidden, HttpResponseRedirect

from .forms import Add_pulse_Form
from django.db.models import Avg, Min, Max, Count

from django.core.paginator import Paginator

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test


def check_owner(private_view):

    # @wraps(private_view)
    def owner_view(request, id, *args, **kwargs):
        logged_user = request.user
        record_owner = Pulse.objects.get(pk=id).owner
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
def all_pulses(request):
    logged_user = request.user

    filter_value = request.GET.get('search')
    sort_value = request.GET.get('sort_by', '-creation_date')
    search_category = request.GET.get('filtering_by')

    if filter_value and len(filter_value) > 0:
        query = {f"{search_category}__icontains": filter_value}
        found_pulses = Pulse.objects.filter(owner=logged_user, **query).order_by(sort_value)
    else:
        found_pulses = Pulse.objects.filter(owner=logged_user).order_by(sort_value)

    page_num = request.GET.get('page', 1)
    pages = Paginator(found_pulses, 5)

    pages_max = pages.num_pages
    pages_max_elements = pages.count
    page_results = pages.get_page(page_num)

    value_y = found_pulses.values_list('pulse', flat=True)
    chart_y = [float(y) for y in value_y]

    value_x = found_pulses.values_list('creation_date', flat=True)
    chart_x = [x.strftime("%Y-%m-%d %H:%M") for x in value_x]

    context = {
        'filter_value': filter_value,
        'sort_value': sort_value,
        'filtering_by': search_category,
        'pages_max': pages_max,
        'pages_max_elements': pages_max_elements,
        'pulses': page_results,
        'chart_x': chart_x,
        'chart_y': chart_y
    }
    return render(request,'app_pulse/all_pulses.html', context)

@login_required
@check_owner
def pulse_details(request, id):
    logged_user = request.user
    found_pulses = Pulse.objects.filter(owner=logged_user)
    pulse_statistical_data = found_pulses.aggregate(Avg('pulse'), Min('pulse'), Max('pulse'), Count('pulse'))

    number = request.POST.get('number')
    found_pulse = Pulse.objects.get(pk=id)

    current_element_index = 0
    for i,g in enumerate(found_pulses):
        if g.id == found_pulse.id:
            current_element_index = i
            break

    first_detail = current_element_index == 0
    last_detail = current_element_index == len(found_pulses) - 1

    prev_view = found_pulses[current_element_index - 1] if not first_detail else None
    next_view = found_pulses[current_element_index + 1] if not last_detail else None
    first_view = found_pulses[0] if not first_detail else None
    last_view = found_pulses[len(found_pulses) - 1] if not last_detail else None
    all_element_index = len(found_pulses)
    number = current_element_index + 1

    if not found_pulse:
        return HttpResponseNotFound('Zasób nie został znaleziony')
    context = {
        'number': number,
        'pulse': found_pulse,
        'statistical_data': pulse_statistical_data,
        'prev_view': prev_view,
        'next_view': next_view,
        'first_view': first_view,
        'last_view': last_view,
        'current_element_index': current_element_index + 1,
        'all_element_index': all_element_index,
    }
    return render(request,'app_pulse/pulse_details.html', context)

@login_required
def add_pulse(request):
    logged_user = request.user
    if request.method == 'POST':
        pulse = request.POST['pulse']
        date = request.POST['date']
        comments = request.POST['comment']
        Pulse.objects.create(pulse=pulse, creation_date=date, comments=comments, owner=logged_user)

        login_history = LoginHistory.objects.filter(user=logged_user).last()
        login_history.cnt_entries +=1
        login_history.save()
        return redirect('all_pulses_url')

    context = {
        'time_value': datetime.now().strftime("%Y-%m-%dT%H:%M"),
        'time_max': datetime.now().strftime("%Y-%m-%dT%H:%M"),
        'time_min': (datetime.now() - timedelta(weeks=52)).strftime("%Y-%m-%dT%H:%M")
    }
    return render(request, 'app_pulse/add_pulse.html', context)

@login_required
@check_owner
def edit_pulse(request, id):
    logged_user = request.user
    found_pulses = Pulse.objects.filter(owner=logged_user)
    found_pulse = Pulse.objects.get(pk=id)

    current_element_index = 0
    for i,g in enumerate(found_pulses):
        if g.id == found_pulse.id:
            current_element_index = i
            break
    number = current_element_index + 1

    if request.method == 'POST':
        pulse = request.POST['pulse']
        date = request.POST['date']
        comments = request.POST['comment']
        found_pulse.delete()
        Pulse.objects.create(pk=id, pulse=pulse, creation_date=date, comments=comments, owner=logged_user)

        login_history = LoginHistory.objects.filter(user=logged_user).last()
        login_history.cnt_modification +=1
        login_history.save()
        return redirect('all_pulses_url')

    context = {
        'pulse': found_pulse,
        'number': number,
        'time_value': found_pulse.creation_date.strftime("%Y-%m-%dT%H:%M"),
        'time_max': datetime.now().strftime("%Y-%m-%dT%H:%M"),
        'time_min': (datetime.now() - timedelta(weeks=52)).strftime("%Y-%m-%dT%H:%M")
    }
    return render(request, 'app_pulse/edit_pulse.html', context)

@login_required
@check_owner
def delete_pulse(request, id):
    logged_user = request.user
    found_pulse = Pulse.objects.get(pk=id)
    found_pulse.delete()

    login_history = LoginHistory.objects.filter(user=logged_user).last()
    login_history.cnt_deleted += 1
    login_history.save()
    return redirect('all_pulses_url')

@login_required
def delete_all_pulse(request):
    logged_user = request.user
    found_pulses = Pulse.objects.filter(owner=logged_user)
    found_pulses.delete()

    login_history = LoginHistory.objects.filter(user=logged_user).last()
    login_history.cnt_all_deleted += 1
    login_history.save()
    return redirect('all_pulses_url')
