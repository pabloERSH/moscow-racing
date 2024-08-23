from django.contrib.auth.views import LoginView
from django.shortcuts import render

from .forms import RegisterUserForm, LoginUserForm

menu = {
    "Трасса": "/track",
    "Автомобили": "/cars",
    'Аренда': '/rent',
}


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация', 'menu': menu}

    # def get_success_url(self):
    #     return reverse_lazy('track')


def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request, 'users/register_done.html', context={'title': 'Сообщение', 'menu': menu})
    else:
        form = RegisterUserForm()
    data = {
        'title': 'Регистрация',
        'menu': menu,
        'form': form
    }
    return render(request, 'users/register.html', context=data)
