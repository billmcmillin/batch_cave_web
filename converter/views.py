from django.http import HttpResponse
from django.shortcuts import render

def home_page(request):
    return render(request, 'home.html')

def create(request):
    return render(request, 'create.html', {
        'new_conversion_text': request.POST.get('conversion_name', ''),
    })
