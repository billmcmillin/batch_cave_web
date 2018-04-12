from django.db import models
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from converter.modelsdir import batchEdits
import inspect
from django.conf import settings

class Conversion(models.Model):
    Name = models.TextField(default='')
    TYPE_CHOICES = [
        (0, 'None'),
    ]
    #get all functions from the BatchEdits
    functions = inspect.getmembers(batchEdits.batchEdits,inspect.isfunction)
    for idx, item in enumerate(functions):
        TYPE_CHOICES.append((idx+1, item[0]))
    Type = models.IntegerField(choices=TYPE_CHOICES,default=0)
    ConvName = models.TextField(default='None')
    #file object for uploaded marc file
    #NOTE - ensure this is outside the server doc root
    upload_storage = FileSystemStorage(location=settings.MEDIA_ROOT,base_url='/data')
    Upload = models.FileField(upload_to='infiles/', storage=upload_storage,default=None)
