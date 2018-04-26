from django.db import models
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from converter.modelsdir import batchEdits
import inspect
from django.conf import settings
from django.core.exceptions import ValidationError
import datetime
import pymarc
from pymarc import MARCReader
from converter.modelsdir import batchEdits
from converter.modelsdir.utilities import utilityFunctions
import os

TYPE_CHOICES = [
    (0, 'None'),
]
#get all functions from the BatchEdits
functions = inspect.getmembers(batchEdits.batchEdits,inspect.isfunction)
for idx, item in enumerate(functions[:-1]):
    TYPE_CHOICES.append((idx+1, item[0]))

class ValidateOnSaveMixin(object):
#from https://www.xormedia.com/django-model-validation-on-save/
    def save(self, force_insert=False, force_update=False, **kwargs):
        if not (force_insert or force_update):
            self.TimeExecuted = datetime.datetime.now(datetime.timezone.utc)
            #self.full_clean()
        super(ValidateOnSaveMixin, self).save(force_insert, force_update,
**kwargs)

class Conversion(ValidateOnSaveMixin, models.Model):
    Name = models.TextField(default='')
    Type = models.IntegerField(choices=TYPE_CHOICES,default=0)
    TimeExecuted = models.DateTimeField(null=True)
    ConvName = models.TextField(default='None')
    #file object for uploaded marc file
    #NOTE - ensure this is outside the server doc root
    upload_storage = FileSystemStorage(location=settings.MEDIA_ROOT,base_url='/data')
    Upload = models.FileField(upload_to='infiles/', storage=upload_storage,default=None)
    MrkIn = models.FileField(upload_to='infiles/', storage=upload_storage,default=None)
    download_storage = FileSystemStorage(location=settings.MEDIA_ROOT,base_url='/data')
    Output = models.FileField(upload_to='outfiles/', storage=download_storage,default=None)
    MrkOut = models.FileField(upload_to='outfiles/', storage=download_storage,default=None)
    RecordsIn = models.PositiveIntegerField(default=0)
    RecordsOut = models.PositiveIntegerField(default=0)

    def clean(self):
        if self.Name is None:
            raise ValidationError('Each conversion must have a name.')
        if self.Upload is None:
            raise ValidationError('Each conversion must have a file uploaded.')
        if self.check_file_make_conversion() != 0:
            raise ValidationError('MARC file does not validate')
        if self.Type == 0:
            raise ValidationError('Type must not be none.')

    def check_file_make_conversion(self):
        check_reader = MARCReader(self.Upload)
        try:
            for record in check_reader:
                self.RecordsIn += 1
        except:
            return 1
        self.make_conversion()
        return 0

    def make_conversion(self):
        #create a new batchEdits object
        BatchEdits = batchEdits.batchEdits()
        #get the name of the method
        self.ConvName = TYPE_CHOICES[self.Type][1]
        #get the callable method from the batchEdits object
        method_to_call = getattr(BatchEdits, self.ConvName)
        #pass the input file to the method and get back BytesIO
        #conv_file = method_to_call('data/infiles/' + self.Upload.name)
        self.Upload.save(self.Upload.name, self.Upload.file, save=False)
        conv_file = method_to_call(self.Upload.path)
        #turn the BytesIO into a file Django can save
        django_output_mrc_file = File(conv_file)
        self.Output.save("Conversion_Results.mrc", django_output_mrc_file, save=False)
        #save input MRK
        input_mrk = BatchEdits.utilities.CreateMRK(self.Upload.path)
        django_input_mrk_file = File(input_mrk)
        self.MrkIn.save("Conversion_Input.mrk", django_input_mrk_file, save=False)
        #save output MRK
        django_output_mrk = BatchEdits.utilities.CreateMRK(self.Output.path)
        self.MrkOut.save("Conversion_Results.mrk", django_output_mrk, save=False)

    def upload_filename(self):
        return os.path.basename(self.Upload.name)

    class Meta:
        ordering = ['-TimeExecuted']
