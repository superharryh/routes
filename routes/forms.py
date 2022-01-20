from django import forms

from cities.models import City
from .models import Route
from trains.models import Train
class RouteForm(forms.Form):
    from_city = forms.ModelChoiceField(
        label='Откуда', queryset=City.objects.all(), widget=forms.Select(
            attrs={'class': 'form-control js-example-basic-single'}
        )
    )
    to_city = forms.ModelChoiceField(
        label='Куда', queryset=City.objects.all(), widget=forms.Select(
            attrs={'class': 'form-control js-example-basic-single'}
        )
    )
    cities = forms.ModelMultipleChoiceField(
        label='Через города', queryset=City.objects.all(),
        required=False, widget=forms.SelectMultiple(
            attrs={'class': 'form-control js-example-basic-multiple'}
        )
    )

    all_travel_time = forms.IntegerField(
        label='Общее время в пути', widget=forms.NumberInput(attrs={
            'class': 'form-control', 'placeholder': 'Время в пути'}
        )
    )

    class Meta:
        model = Route
        fields = ('from_city', 'to_city', 'cities', 'all_travel_time')


# эта форма (пустой каркас из полей) будет заполнена в def add_route(request): in routes/views.py и уже add_route(request) будет указываться в project/urls.py
class RouteModelForm(forms.ModelForm): # используется только в def add_route(request): in routes/views.py
    name = forms.CharField(label='Название маршрута', widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Введите название маршрута'}
        )
    ) # только name будет отображаться на странице routes/create.html и его нужно будет заполнить (т.е. придумать имя для выбранного маршрута)
    
    # все эти поля уже заполнены def add_route(request): in routes/views.py и будут невидимы
    from_city = forms.ModelChoiceField(
        queryset=City.objects.all(), widget=forms.HiddenInput()
    )
    to_city = forms.ModelChoiceField(
        queryset=City.objects.all(), widget=forms.HiddenInput()
    )
    trains = forms.ModelMultipleChoiceField(
        queryset=Train.objects.all(),
        required=False, widget=forms.SelectMultiple(
            attrs={'class': 'form-control d-none'} # тут HiddenInput() не подойдет, так как SelectMultiple() => d-none - просто не будет отображать данное поле 
        )
    )
    travel_times = forms.IntegerField(
        widget=forms.HiddenInput()
    )

    class Meta:
        model = Route
        fields = '__all__'