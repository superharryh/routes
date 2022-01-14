from django import forms

from .models import City

class CityForm(forms.ModelForm):
    name = forms.CharField(label='Город', widget=forms.TextInput(attrs=
                {'class':'form_control',
                'placeholder':'Введите название'}))
    class Meta:
        model = City
        fields = ('name',)
