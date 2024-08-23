from django.urls import path, re_path, register_converter
from . import views  # . means import from current module

urlpatterns = [
    path('track/', views.track, name='track'),
    path('add_rate/', views.add_rate, name='add_rate'),
    path('rent/', views.rent_form, name='rent_form'),
    path('cars/', views.auto, name='cars'),
    path('', views.home),
]
