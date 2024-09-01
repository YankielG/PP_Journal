import decimal
from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from .models import Weight
from app_growth.models import Growth
from django.http import HttpResponseNotFound, HttpResponseForbidden
from .forms import Add_weight_Form
from django.db.models import Avg, Min, Max, Count

from django.core.paginator import Paginator

# Create your views here.
def all_weights(request):
    found_weights = Weight.objects.all().order_by('date')
    page_num = request.GET.get('page', 1)
    pages = Paginator(found_weights, 3)

    pages_max = pages.num_pages
    pages_max_elements = pages.count
    page_results = pages.get_page(page_num)

    value_y = Weight.objects.values_list('weight', flat=True)
    chart_y = [float(y) for y in value_y]

    value_x =found_weights.values_list('date', flat=True)
    chart_x = [x.strftime("%Y-%m-%d %H:%M") for x in value_x]

    context = {
        'pages_max': pages_max,
        'pages_max_elements': pages_max_elements,
        'weights': page_results,
        'chart_x': chart_x,
        'chart_y': chart_y
    }
    return render(request,'app_weight/all_weights.html', context)

def weight_details(request, id):
    found_weights = Weight.objects.all()
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

def add_weight(request):
    if request.method == 'POST':
        weight = request.POST['weight']
        date = request.POST['date']
        comments = request.POST['comment']
        object = Weight(weight=weight, date=date, comments=comments)
        object.save()
        return redirect('all_weights_url')

    context = {
        'time_value': datetime.now().strftime("%Y-%m-%dT%H:%M"),
        'time_max': datetime.now().strftime("%Y-%m-%dT%H:%M"),
        'time_min': (datetime.now() - timedelta(weeks=52)).strftime("%Y-%m-%dT%H:%M")
    }
    return render(request, 'app_weight/add_weight.html',context)

def edit_weight(request, id):
    found_weight = Weight.objects.get(pk=id)
    if request.method == 'POST':
        # found_weight.weight = request.POST['weight']
        # found_weight.date = request.POST['date']
        # found_weight.comments = request.POST['comment']
        # found_weight.save()
        weight = request.POST['weight']
        date = request.POST['date']
        comments = request.POST['comment']
        found_weight.delete()
        Weight.objects.create(pk=id, weight=weight, date=date, comments=comments)
        return redirect('all_weights_url')

    context = {
        'weight': found_weight,
        'time_value': found_weight.date.strftime("%Y-%m-%dT%H:%M"),
        'time_max': datetime.now().strftime("%Y-%m-%dT%H:%M"),
        'time_min': (datetime.now() - timedelta(weeks=52)).strftime("%Y-%m-%dT%H:%M")
    }
    return render(request, 'app_weight/edit_weight.html', context)


def delete_weight(request, id):
    found_weight = Weight.objects.get(pk=id)
    found_weight.delete()
    return redirect('all_weights_url')


def delete_all_weight(request):
    found_weights = Weight.objects.all()
    found_weights.delete()
    return redirect('all_weights_url')


def info(request):
    return  render(request,'app_weight/info.html')


def error(request):
    return  render(request, '404.html')


def home(request):
    found_weights = Weight.objects.all()
    found_growth = Growth.objects.all()

    if found_weights and found_growth:
        last_weight = Weight.objects.latest('date')
        last_growth = Growth.objects.latest("date")
        bmi_value = float(round(last_weight.weight / (last_growth.growth/100 * last_growth.growth/100), 2))
        value_chart = 50 - bmi_value
        chart = [bmi_value, value_chart]
    else:
        bmi_value = 0
        value_chart = 50 - bmi_value
        chart = [bmi_value, value_chart]

    bmi_rate = 'Brak Oceny'
    bmi_color = '#CD853F'
    bmi_comment = 'Dokonaj wpisów wagi i wzrostu, BMI to: masa / wzrost * 2'
    if bmi_value < 5:
        pass
    elif bmi_value < 18.5 :
        bmi_rate = 'Niskie'
        bmi_color = '#0000FF'
        bmi_comment = 'Twoje BMI jest za niskie, jedź więcej. Skonsultuj sie z lekarzem.'
    elif bmi_value < 25:
        bmi_rate = 'W normie'
        bmi_color = '#32CD32'
        bmi_comment = 'Twoje BMI OK tak trzymaj.'
    elif bmi_value < 30:
        bmi_rate = 'Wysokie'
        bmi_color = '#FFA500'
        bmi_comment = 'Twoje BMI przekracza limit. Muszisz więcej ćwiczyć, aby poprawić sylwetkę'
    else:
        bmi_rate = 'Bardzo Wysokie'
        bmi_color = '#FF0000'
        bmi_comment = 'Twoje BMI przekracza limit. Muszisz więcej ćwiczyć i stosować dietę. Skonsultuj sie z lekarzem.'


    context = {
        'chart': chart,
        'bmi_value': bmi_value,
        'bmi_rate': bmi_rate,
        'bmi_color': bmi_color,
        'bmi_comment': bmi_comment
    }
    return  render(request,'app_weight/home.html', context)
