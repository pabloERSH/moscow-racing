from datetime import date, timedelta

from django import forms

from .models import Rentals, Cars


def GenerateDates():
    num_days = 5
    start_date = date.today()
    dateframe = [start_date + timedelta(days=d) for d in range(num_days)]
    dates = [('', 'Выберите дату')]
    cars_cnt = Cars.objects.count()
    for i in range(len(dateframe)):
        if Rentals.objects.filter(RentDate=dateframe[i]).count() < cars_cnt*3:
            dates.append((dateframe[i], dateframe[i].strftime("%d.%m.%Y")))
    return dates


def GenerateCars():
    cars = [('', 'Выберите авто')]
    cars_cnt = Cars.objects.all()
    for car in cars_cnt:
        cars.append((car, car))
    return cars


class AddRental(forms.ModelForm):
    RentDate = forms.ChoiceField(label='Дата: ',
                                 choices=GenerateDates(),
                                 error_messages={
                                     'required': 'Выберите дату!'})
    RentTime = forms.ChoiceField(label='Время: ',
                                 choices=[('', 'Выберите время'),
                                          ('10:00-12:00', '10:00-12:00'),
                                          ('13:00-15:00', '13:00-15:00'),
                                          ('16:00-18:00', '16:00-18:00'),
                                          ],
                                 error_messages={
                                     'required': 'Выберите время!'})
    Car = forms.ChoiceField(label='Авто: ',
                            choices=GenerateCars(),
                            error_messages={
                                'required': 'Выберите авто!'})

    class Meta:
        model = Rentals
        fields = ['ClientName', 'ClientEmail', 'RentDate', 'RentTime', 'Car']
        widgets = {
            'ClientName': forms.TextInput(attrs={'id': 'name',
                                                 'type': 'text',
                                                 'class': 'form-input',
                                                 'name': 'name'}),
            'ClientEmail': forms.EmailInput(attrs={'id': 'email',
                                                   'type': 'email',
                                                   'class': 'form-input',
                                                   'name': 'email'}),
            'RentDate': forms.Select(attrs={'id': 'date',
                                            'name': 'date'}),
            'RentTime': forms.Select(attrs={'id': 'time',
                                            'name': 'time'}),
            'Car': forms.Select(attrs={'id': 'car',
                                       'name': 'car'})
        }

        error_messages = {
            'ClientName': {'required': 'Введите имя!'},
            'ClientEmail': {'required': 'Введите email!',
                            'valid': 'Некорректный email!'},
        }
