from django.shortcuts import render


menu = {
    "Трасса": "/track",
    "Автомобили": "/cars",
    'Аренда': '/rent',
}


def page_not_found_view(request, exception):
    data = {
        'menu': menu,
        'title': 'Ошибка 404'
    }
    return render(request, '404.html', status=404, context=data)
