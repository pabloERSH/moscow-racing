from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm


class LoginUserForm(AuthenticationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'password']
        labels = {
            'username': 'Логин: ',
            'password': 'Пароль: '
        }
        error_messages = {
            'username': {'required': 'Введите логин!'},
            'password': {'required': 'Введите пароль!'}
        }


class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(label='Логин: ',
                               error_messages={'required': 'Введите логин!'})
    password = forms.CharField(label='Пароль: ', widget=forms.PasswordInput(attrs={'class': 'form-input'}),
                               error_messages={'required': 'Введите пароль!'})
    password2 = forms.CharField(label='Повтор пароля: ', widget=forms.PasswordInput(attrs={'class': 'form-input'}),
                                error_messages={'required': 'Повторите пароль!'})

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']
        labels = {
            'email': 'Почта: ',
            'first_name': 'Имя: ',
            'last_name': 'Фамилия: '
        }
        error_messages = {
            'username': {'required': 'Введите логин!'},
            'email': {'required': 'Введите email!'},
            'password': {'required': 'Введите пароль!'},
            'password2': {'required': 'Повторите пароль!'}
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Пароли не совпадают!")
        return cd['password']

    def clean_email(self):
        email = self.cleaned_data['email']
        if email and get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Аккаунт с таким Email уже существует!")
        return email
