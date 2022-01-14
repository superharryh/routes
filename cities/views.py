from django.shortcuts import render

# Create your views here.
def cities(request):
    cities_qs = City.objects.all()
    context = {'cities_list': cities_qs}
    return render(request, 'cities/cities.html', context)