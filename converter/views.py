from django.shortcuts import redirect, render
from converter.models import Conversion

def home_page(request):
    return render(request, 'home.html')

def index(request):
    convs = Conversion.objects.all()
    return render(request, 'index.html', {'Conversions': convs})

def create(request):
    if request.method == 'POST':
        Conversion.objects.create(Name=request.POST['conversion_name'])
        return redirect('/conversions/index')

    return render(request, 'create.html')

