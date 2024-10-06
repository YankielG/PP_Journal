from datetime import datetime, timedelta
from functools import wraps

from django.shortcuts import render, redirect, get_object_or_404
from django.template.context_processors import request

from .models import Weight
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
@check_owner
# @csrf_exempt
def weight_details(request, id):
    logged_user = request.user
    found_weights = Weight.objects.filter(owner=logged_user).order_by('-creation_date')
    weight_statistical_data = found_weights.aggregate(Avg('weight'), Min('weight'), Max('weight'), Count('weight'))
    number = request.POST.get('number')
    found_weight = Weight.objects.get(pk=id)
    # csrf_token = get_token(request)

    current_element_index = 0
    for i,g in enumerate(found_weights):
        if g.id == found_weight.id:
            current_element_index = i
            print(i)
            print(g)
            print(found_weights)
            break

    first_detail= current_element_index == 0
    last_detail = current_element_index == len(found_weights) - 1

    prev_view = found_weights[current_element_index - 1] if not first_detail else None
    next_view = found_weights[current_element_index + 1] if not last_detail else None
    first_view = found_weights[0] if not last_detail else None
    last_view = found_weights[last_detail] if not last_detail else None

    page_num = request.GET.get('page')

    if not found_weight:
        return HttpResponseNotFound('Zasób nie został znaleziony')
    context = {
        'number': number,
        'weight': found_weight,
        'statistical_data': weight_statistical_data,
        'prev_view': prev_view,
        'next_view': next_view,
        'page_num': page_num,
        'first_view': first_view,
        'last_view': last_view,
        'last_detail': len(found_weights),
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
@check_owner
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
@check_owner
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
