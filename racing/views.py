import json
from idlelib.iomenu import errors

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView
from .forms import AddRental
from .models import Rates, Cars, Rentals


menu = {
    "Трасса": "/track",
    "Автомобили": "/cars",
    'Аренда': '/rent',
}


def track(request):
    data = {
        'title': 'Трек',
        'menu': menu,
    }
    return render(request, 'racing/track.html', context=data)


def home(request):
    return redirect('track')


@login_required
def rent_form(request):
    msg = ''
    form_errors = []
    success = False
    if request.method == 'POST':
        date = request.POST.get('RentDate')
        time = request.POST.get('RentTime')
        car = request.POST.get('Car')
        form = AddRental(request.POST)
        if form.is_valid():
            if not Rentals.objects.filter(RentDate=date, RentTime=time, Car=car).exists():
                my_model_instance = form.save(commit=False)
                my_model_instance.User = request.user
                my_model_instance.save()
                msg = f"{request.POST.get('ClientName')}, вы успешно забронировали трек!"
                success = True
            else:
                msg = f'На {date} {time} машина {car} уже забронирована, выберите другую машину!'
        else:
            form_errors = form.errors
    else:
        form = AddRental()
    data = {
        'title': 'Аренда',
        'menu': menu,
        'msg': msg,
        'form': form,
        'success': success,
        'form_errors': form_errors
    }
    return render(request, 'racing/rent.html', context=data)


def count_rating_info(car_id):
    if Rates.objects.filter(pk__isnull=False).exists():
        avg_sum = Rates.objects.filter(car=car_id).aggregate(Avg('rate'))['rate__avg']
        cnt = Rates.objects.filter(car=car_id).count()
        return cnt, avg_sum
    else:
        return 0, 0


def auto(request):
    cars_info = Cars.objects.all()
    cars_info_list = list(cars_info.values())
    for i in range(len(cars_info_list)):
        count, avg_sum = count_rating_info(cars_info_list[i]['id'])
        cars_info_list[i]['count'] = count
        cars_info_list[i]['avg_sum'] = str(round(avg_sum, 2)).replace(',', '.')

    data = {
        'title': 'Автопарк',
        'menu': menu,
        'cars_info': cars_info_list,
        }
    return render(request, 'racing/cars.html', context=data)


@csrf_exempt
def add_rate(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            data = json.loads(request.body)
            value = int(data.get('userRating', 0))
            car_id = int(data.get('carId', 0))
            car = Cars.objects.get(id=car_id)
            filters = {
                'car': car,
                'user': request.user.id
            }
            if Rates.objects.filter(**filters).exists():
                Rates.objects.filter(**filters).update(rate=value)
            else:
                new_rate = Rates.objects.create(rate=value, user=request.user, car=car)
                new_rate.save()

            avg_sum = Rates.objects.filter(car=car).aggregate(Avg('rate'))['rate__avg']
            cnt = Rates.objects.filter(car=car).count()
            return JsonResponse({'newRating': round(avg_sum, 2), 'newCount': cnt, 'type': 'answer'})
        else:
            return JsonResponse({'type': 'error', 'message': 'Чтобы проголосовать, требуется авторизация!!!'})
