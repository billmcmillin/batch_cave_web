from django.shortcuts import redirect, render
from converter.models import Conversion
from converter.forms import ConversionForm

def home_page(request):
    return render(request, 'home.html')

def index(request):
    convs = Conversion.objects.all()
    return render(request, 'index.html', {'Conversions': convs})

def create(request):
    if request.method == 'POST':
        formObj = ConversionForm(request.POST, request.FILES)
        if formObj.is_valid():
            formObj.save()
            return redirect('/conversions/index')
    else:
        formObj = ConversionForm()

    return render(request, 'create.html', {'form':  formObj})

