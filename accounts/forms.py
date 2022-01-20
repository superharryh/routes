from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password

#* 1.) Создаем форму для логина юзера:
User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField(
        label='username', widget=forms.TextInput(
            attrs={'class': 'form-control',
            'placeholder': 'Введите username'}
        )
    )

    password = forms.CharField(
        label='password', widget=forms.PasswordInput(
            attrs={'class': 'form-control',
            'placeholder': 'Введите username'}
        )
    )

    # проводим внутреннюю проверку юзера, после того как он нажал кнопку "войти":
    def clean(self, *args, **kwargs):
        # получаем данные, ввеленные пользователем 
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password: # если были введены и username и password:
            qs = User.objects.filter(username=username) # находим юзера по username
            if not qs.exists(): # если он не зарегистрирован (нет в БД):
                raise forms.ValidationError('Такого пользователя нет') # ошибка
            # проверяем совпадение passwords: но passwords шифруемые (хэшированные) => надо заносить в функцию check_password пароль, введнный юзером и пароль из БД, полученный по User:
            if not check_password(password, qs[0].password): # если юзер ввел не верный пароль:
                raise forms.ValidationError('Неверный пароль') # ошибка
            # юзер ввел верные и username и пароль => надо аутентифицировать юзера:
            user = authenticate(username=username, password=password)

            # Если юзер активный, то мы получим экземпляр юзера, если он не активный, то - None:
            if not user:
                raise forms.ValidationError('Данный пользователь неактивен')
        
        # когда все удовлетворяет условиям, то пропускаем данные пользователь через всю внутренню структуру Django:
        return super().clean(*args, **kwargs)


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        label='username', widget=forms.TextInput(
            attrs={'class': 'form-control',
            'placeholder': 'Введите username'}
        )
    )

    password = forms.CharField(
        label='password', widget=forms.PasswordInput(
            attrs={'class': 'form-control',
            'placeholder': 'Введите username'}
        )
    )

    password2 = forms.CharField(
        label='password', widget=forms.PasswordInput(
            attrs={'class': 'form-control',
            'placeholder': 'Введите username'}
        )
    )

    class Meta:
        model = User
        fields = ('username',) # из модели User мы берем только username
    
    # проверяем совпадение двух пароль:
    def clean_password2(self):
        data = self.cleaned_data
        if data['password'] != data['password2']:
            raise forms.ValidationError('Пароли не совпадают')

        return data['password2']





