from django import forms

from .models import Train
from cities.models import City

class TrainForm(forms.ModelForm):
    name = forms.CharField(label='Номер поезда', widget=forms.TextInput(attrs=
                {'class':'form_control',
                'placeholder':'Введите номер поезда'}))

    from_city = forms.ModelChoiceField(label='Откуда', 
                                        queryset=City.objects.all(),
                                        widget=forms.Select(attrs={'class':'form_control'})) 

    to_city = forms.ModelChoiceField(label='Куда', 
                                        queryset=City.objects.all(),
                                        widget=forms.Select(attrs={'class':'form_control'})) 

    
    travel_time = forms.IntegerField(label='Время в пути', widget=forms.NumberInput(attrs=
                {'class':'form_control',
                'placeholder':'Минуты'}))

    class Meta:
        model = Train
        fields = '__all__'
