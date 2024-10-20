from datetime import datetime, timedelta
from functools import wraps

from django.shortcuts import render, redirect, get_object_or_404
from django.template.context_processors import request

from .models import Growth
from app_users.models import LoginHistory
from django.http import HttpResponseNotFound, HttpResponseForbidden, HttpResponseRedirect

from .forms import Add_growth_Form
from django.db.models import Avg, Min, Max, Count

from django.core.paginator import Paginator

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test


def check_owner(private_view):

    # @wraps(private_view)
    def owner_view(request, id, *args, **kwargs):
        logged_user = request.user
        record_owner = Growth.objects.get(pk=id).owner
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
def all_growths(request):
    logged_user = request.user

    filter_value = request.GET.get('search', '')
    sort_value = request.GET.get('sort_by', '-creation_date')
    search_category = request.GET.get('filtering_by', '')

    if filter_value and len(filter_value) > 0:
        query = {f"{search_category}__icontains": filter_value}
        found_growths = Growth.objects.filter(owner=logged_user, **query).order_by(sort_value)
    else:
        found_growths = Growth.objects.filter(owner=logged_user).order_by(sort_value)

    # if sort_value is None:
    #     sort_value = ''
    # if filter_value is None:
    #     filter_value = ''
    # if search_category is None:
    #     search_category = ''

    page_num = request.GET.get('page', 1)
    pages = Paginator(found_growths, 5)

    pages_max = pages.num_pages
    pages_max_elements = pages.count
    page_results = pages.get_page(page_num)

    value_y = found_growths.values_list('growth', flat=True)
    chart_y = [float(y) for y in value_y]

    value_x = found_growths.values_list('creation_date', flat=True)
    chart_x = [x.strftime("%Y-%m-%d %H:%M") for x in value_x]

    context = {
        'filter_value': filter_value,
        'sort_value': sort_value,
        'filtering_by': search_category,
        'pages_max': pages_max,
        'pages_max_elements': pages_max_elements,
        'growths': page_results,
        'chart_x': chart_x,
        'chart_y': chart_y,
    }
    return render(request,'app_growth/all_growths.html', context)

@login_required
@check_owner
def growth_details(request, id):
    logged_user = request.user
    found_growths = Growth.objects.filter(owner=logged_user)
    growth_statistical_data = found_growths.aggregate(Avg('growth'), Min('growth'), Max('growth'), Count('growth'))

    number = request.POST.get('number')
    found_growth = Growth.objects.get(pk=id)

    current_element_index = 0
    for i,g in enumerate(found_growths):
        if g.id == found_growth.id:
            current_element_index = i
            break

    first_detail = current_element_index == 0
    last_detail = current_element_index == len(found_growths) - 1

    prev_view = found_growths[current_element_index - 1] if not first_detail else None
    next_view = found_growths[current_element_index + 1] if not last_detail else None
    first_view = found_growths[0] if not first_detail else None
    last_view = found_growths[len(found_growths) - 1] if not last_detail else None
    all_element_index = len(found_growths)
    number = current_element_index + 1

    if not found_growth:
        return HttpResponseNotFound('Zasób nie został znaleziony')
    context = {
        'number': number,
        'growth': found_growth,
        'statistical_data': growth_statistical_data,
        'prev_view': prev_view,
        'next_view': next_view,
        'first_view': first_view,
        'last_view': last_view,
        'current_element_index': current_element_index + 1,
        'all_element_index': all_element_index,
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

        login_history = LoginHistory.objects.filter(user=logged_user).last()
        login_history.cnt_entries +=1
        login_history.save()
        return redirect('all_growths_url')

    context = {
        'time_value': datetime.now().strftime("%Y-%m-%dT%H:%M"),
        'time_max': datetime.now().strftime("%Y-%m-%dT%H:%M"),
        'time_min': (datetime.now() - timedelta(weeks=52)).strftime("%Y-%m-%dT%H:%M")
    }
    return render(request, 'app_growth/add_growth.html', context)

@login_required
@check_owner
def edit_growth(request, id):
    logged_user = request.user
    found_growths = Growth.objects.filter(owner=logged_user).order_by('-creation_date')
    found_growth = Growth.objects.get(pk=id)

    current_element_index = 0
    for i,g in enumerate(found_growths):
        if g.id == found_growth.id:
            current_element_index = i
            break
    number = current_element_index + 1

    if request.method == 'POST':
        found_growth.growth = request.POST['growth']
        found_growth.creation_date = request.POST['date']
        found_growth.comments = request.POST['comment']
        found_growth.cnt_modification +=1
        found_growth.save()

        login_history = LoginHistory.objects.filter(user=logged_user).last()
        login_history.cnt_modification +=1
        login_history.save()
        return redirect('all_growths_url')

    context = {
        'growth': found_growth,
        'number': number,
        'time_value': found_growth.creation_date.strftime("%Y-%m-%dT%H:%M"),
        'time_max': datetime.now().strftime("%Y-%m-%dT%H:%M"),
        'time_min': (datetime.now() - timedelta(weeks=52)).strftime("%Y-%m-%dT%H:%M")
    }
    return render(request, 'app_growth/edit_growth.html', context)

@login_required
@check_owner
def delete_growth(request, id):
    logged_user = request.user
    found_growth = Growth.objects.get(pk=id)
    found_growth.delete()

    login_history = LoginHistory.objects.filter(user=logged_user).last()
    login_history.cnt_deleted += 1
    login_history.save()
    return redirect('all_growths_url')

@login_required
def delete_all_growth(request):
    logged_user = request.user
    found_growths = Growth.objects.filter(owner=logged_user)
    found_growths.delete()

    login_history = LoginHistory.objects.filter(user=logged_user).last()
    login_history.cnt_all_deleted += 1
    login_history.save()
    return redirect('all_growths_url')
