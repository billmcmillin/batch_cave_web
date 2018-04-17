from django.shortcuts import redirect, render
from converter.models import Conversion
from converter.forms import ConversionForm
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def home_page(request):
    return render(request, 'home.html')

def index(request):
    convs = Conversion.objects.all()
    page_num = request.GET.get('page', 1)
    paginator = Paginator(convs, 10)
    try:
        conversions_out = paginator.page(page_num)
    except PageNotAnInteger:
        conversions_out = paginator.page(1)
    except EmptyPage:
        conversions_out = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'Conversions': conversions_out})

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

def download(request, conversion_id):
    convo = Conversion.objects.get(pk=conversion_id)
    response = HttpResponse(convo.Output)
    response['content_type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename=%s' % convo.Name
    return response

def download_original(request, conversion_id):
    convo = Conversion.objects.get(pk=conversion_id)
    response = HttpResponse(convo.Upload)
    response['content_type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename=%s' % convo.Name
    return response

def download_original_mrk(request, conversion_id):
    convo = Conversion.objects.get(pk=conversion_id)
    response = HttpResponse(convo.MrkIn)
    response['content_type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename=%s' % convo.Name
    return response

def download_result_mrk(request, conversion_id):
    convo = Conversion.objects.get(pk=conversion_id)
    response = HttpResponse(convo.MrkOut)
    response['content_type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename=%s' % convo.Name
    return response
