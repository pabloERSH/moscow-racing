from django.contrib.auth import get_user_model
from django.db import models


class Rentals(models.Model):
    ClientName = models.CharField(max_length=255, default='', verbose_name='Имя: ')
    ClientEmail = models.EmailField(max_length=255, default='', verbose_name='Почта: ')
    RentDate = models.DateField(default=None, verbose_name='Дата: ', null=True)
    RentTime = models.CharField(max_length=11, default='', verbose_name='Время: ')
    Car = models.CharField(max_length=50, default='', verbose_name='Авто: ')
    User = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='User', null=True, default=None)


class Cars(models.Model):
    Car_name = models.CharField(max_length=255, default='')
    Power = models.PositiveIntegerField(default=0)
    Go_to_100 = models.FloatField(default=0)
    Max_speed = models.PositiveIntegerField(default=0)
    Type_of_gsb = models.CharField(max_length=14, default='')
    Type_of_drive = models.CharField(max_length=8, default='')
    Img_of_car = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.Car_name


class Rates(models.Model):
    rate = models.SmallIntegerField(default=0)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user', null=True, default=None)
    car = models.ForeignKey(Cars, on_delete=models.CASCADE, related_name='cars', null=True, default=None)
