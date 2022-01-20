from django.shortcuts import render

# Create your views here.

#* 2.) Создаем функции входа и выхода юзера:

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from .forms import UserLoginForm, UserRegistrationForm
from django.contrib import messages 

def login_view(request):
    form = UserLoginForm(request.POST or None)
    _next = request.GET.get('next')
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        # если страница для переброски после логина зивестна и == _next:
        _next = _next or '/' # or '/' если переменная _next не задана, т.е. в GET ничего нет
        return redirect(_next )
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')

def registration_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False) # пользователь будет добавлен в систему, но ещё до конца не сохранен, цель: хэширование пароля:
            new_user.set_password(form.cleaned_data['password'])
            new_user = form.save() 
            messages.success(request, 'Регистрация прошла успешно!')
            return render(request, 'accounts/register_done.html', {'new_user': new_user})
        return render(request, 'accounts/register.html', {'form': form})
    
    else: # if request.method == 'GET':
        form = UserRegistrationForm()
        return render(request, 'accounts/register.html', {'form': form})
