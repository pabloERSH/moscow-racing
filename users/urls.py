from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views  # . means import from current module
from .views import LoginUser

app_name = "users"

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
]
