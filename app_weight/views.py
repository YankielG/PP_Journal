from datetime import datetime, timedelta
from functools import wraps

from django.shortcuts import render, redirect, get_object_or_404
from django.template.context_processors import request

from .models import Weight
from app_users.models import LoginHistory
from django.http import HttpResponseNotFound, HttpResponseForbidden, HttpResponseRedirect

from .forms import Add_weight_Form
from django.db.models import Avg, Min, Max, Count

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_protect, csrf_exempt


def check_owner(private_view):

    # @wraps(private_view)
    def owner_view(request, id, *args, **kwargs):
        logged_user = request.user
        record_owner = Weight.objects.get(pk=id).owner
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
def all_weights(request):
    logged_user = request.user

    filter_value = request.GET.get('search')
    sort_value = request.GET.get('sort_by', '-creation_date')
    search_category = request.GET.get('filtering_by')

    if filter_value and len(filter_value) > 0:
        query = {f"{search_category}__icontains": filter_value}
        found_weights = Weight.objects.filter(owner=logged_user, **query).order_by(sort_value)
    else:
        found_weights = Weight.objects.filter(owner=logged_user).order_by(sort_value)


    page_num = request.GET.get('page', 1)
    pages = Paginator(found_weights, 5)

    pages_max = pages.num_pages
    pages_max_elements = pages.count
    page_results = pages.get_page(page_num)

    value_y = found_weights.values_list('weight', flat=True)
    chart_y = [float(y) for y in value_y]

    value_x = found_weights.values_list('creation_date', flat=True)
    chart_x = [x.strftime("%Y-%m-%d %H:%M") for x in value_x]

    context = {
        'filter_value' : filter_value,
        'sort_value': sort_value,
        'filtering_by': search_category,
        'pages_max': pages_max,
        'pages_max_elements': pages_max_elements,
        'weights': page_results,
        'chart_x': chart_x,
        'chart_y': chart_y
    }
    return render(request,'app_weight/all_weights.html', context)

@login_required
@check_owner
# @csrf_exempt
def weight_details(request, id):
    logged_user = request.user
    found_weights = Weight.objects.filter(owner=logged_user).order_by('-creation_date')
    weight_statistical_data = found_weights.aggregate(Avg('weight'), Min('weight'), Max('weight'), Count('weight'))

    # if request.method == 'POST':
    #     number = request.POST.get('number')

    found_weight = Weight.objects.get(pk=id)
    # csrf_token = get_token(request)

    current_element_index = 0
    for i,g in enumerate(found_weights):
        if g.id == found_weight.id:
            current_element_index = i
            break

    first_detail = current_element_index == 0
    last_detail = current_element_index == len(found_weights) - 1

    prev_view = found_weights[current_element_index - 1] if not first_detail else None
    next_view = found_weights[current_element_index + 1] if not last_detail else None
    first_view = found_weights[0] if not first_detail else None
    last_view = found_weights[len(found_weights) - 1] if not last_detail else None
    all_element_index = len(found_weights)
    number = current_element_index + 1

    if not found_weight:
        return HttpResponseNotFound('Zasób nie został znaleziony')
    context = {
        'number': number,
        'weight': found_weight,
        'statistical_data': weight_statistical_data,
        'prev_view': prev_view,
        'next_view': next_view,
        'first_view': first_view,
        'last_view': last_view,
        'current_element_index': current_element_index + 1,
        'all_element_index': all_element_index,
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

        login_history = LoginHistory.objects.filter(user=logged_user).last()
        login_history.cnt_entries +=1
        login_history.save()
        return redirect('all_weights_url')

    context = {
        'time_value': datetime.now().strftime("%Y-%m-%dT%H:%M"),
        'time_max': datetime.now().strftime("%Y-%m-%dT%H:%M"),
        'time_min': (datetime.now() - timedelta(weeks=52)).strftime("%Y-%m-%dT%H:%M")
    }
    return render(request, 'app_weight/add_weight.html',context)

@login_required
@check_owner
def edit_weight(request, id):
    logged_user = request.user
    found_weights = Weight.objects.filter(owner=logged_user).order_by('-creation_date')
    found_weight = Weight.objects.get(pk=id)

    current_element_index = 0
    for i,g in enumerate(found_weights):
        if g.id == found_weight.id:
            current_element_index = i
            break
    number = current_element_index + 1

    if request.method == 'POST':
        found_weight.weight = request.POST['weight']
        found_weight.creation_date = request.POST['date']
        found_weight.comments = request.POST['comment']
        found_weight.cnt_modification +=1
        found_weight.save()

        login_history = LoginHistory.objects.filter(user=logged_user).last()
        login_history.cnt_modification +=1
        login_history.save()
        return redirect('all_weights_url')

    context = {
        'weight': found_weight,
        'number': number,
        'time_value': found_weight.creation_date.strftime("%Y-%m-%dT%H:%M"),
        'time_max': datetime.now().strftime("%Y-%m-%dT%H:%M"),
        'time_min': (datetime.now() - timedelta(weeks=52)).strftime("%Y-%m-%dT%H:%M")
    }
    return render(request, 'app_weight/edit_weight.html', context)

@login_required
@check_owner
def delete_weight(request, id):
    logged_user = request.user
    found_weight = Weight.objects.get(pk=id)
    found_weight.delete()

    login_history = LoginHistory.objects.filter(user=logged_user).last()
    login_history.cnt_deleted += 1
    login_history.save()
    return redirect('all_weights_url')

@login_required
def delete_all_weight(request):
    logged_user = request.user
    found_weights = Weight.objects.filter(owner=logged_user)
    found_weights.delete()

    login_history = LoginHistory.objects.filter(user=logged_user).last()
    login_history.cnt_all_deleted += 1
    login_history.save()
    return redirect('all_weights_url')
