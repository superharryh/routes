from django import forms

from .models import Train
from cities.models import City

class TrainForm(forms.ModelForm):
    name = forms.CharField(label='Номер поезда', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите номер поезда'}
        )
    )
    travel_time = forms.IntegerField(
        label='Время в пути', widget=forms.NumberInput(attrs={
            'class': 'form-control', 'placeholder': 'Время в пути'}
        )
    )
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

    class Meta:
        model = Train
        fields = '__all__'
