from django.shortcuts import redirect, render
from converter.models import Conversion
from converter.forms import ConversionForm
from django.core.exceptions import ValidationError

def home_page(request):
    return render(request, 'home.html')

def index(request):
    convs = Conversion.objects.all()
    return render(request, 'index.html', {'Conversions': convs})

def create(request):
    if request.method == 'POST':
        formObj = ConversionForm(request.POST, request.FILES)
        if formObj.is_valid():
            try:
                formObj.full_clean()
                formObj.save()
            except ValidationError as ve:
                error = ve
                return render(request, 'create.html', {"error": error})
            return redirect('/conversions/index')
    else:
        formObj = ConversionForm()

    return render(request, 'create.html', {'form':  formObj})

