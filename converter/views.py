from django.shortcuts import redirect, render
from converter.models import Conversion

def home_page(request):
    return render(request, 'home.html')

def index(request):
    return render(request, 'index.html')

def create(request):
    if request.method == 'POST':
        Conversion.objects.create(name=request.POST['conversion_name'])
        return redirect('/conversions/index')

    return render(request, '/conversions/create.html')

