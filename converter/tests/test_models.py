from django.test import TestCase
from converter.models import Conversion
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from unittest import skip

class ConversionModelTest(TestCase):

    def get_test_file(self):
        with open('data/infiles/TEST.mrc', 'rb') as testMarc:
            test_file = SimpleUploadedFile('TEST.mrc', testMarc.read())
        return test_file

    def get_bad_file(self):
        with open('data/infiles/shell.mrc', 'rb') as testMarc:
            test_file = SimpleUploadedFile('testing_bad_upload.mrc', testMarc.read())
        return test_file

    def open_file(self, file_name):
        test_file = file_name.read()
        return test_file

    def test_get_error_from_invalid_model(self):
        with self.assertRaises(ValueError):
            Conversion(Name='Test1', Type=0, Upload=None).save()

    def test_cannot_save_incomplete_conversion(self):
        conv = Conversion.objects.create()
        with self.assertRaises(ValueError):
            conv.save()

    def test_uploaded_file_saved_is_same_size_in_db(self):
        test_file = self.get_test_file()
        response =self.client.post('/conversions/create/', data={'Name': 'test conversion', 'Type': '2', 'Upload': test_file})
        saved_items = Conversion.objects.all()
        saved_file = saved_items[0].Upload
        self.assertEqual(saved_file._get_size(), test_file._get_size())

    def test_conversion_name_is_saved(self):
        test_file = self.get_test_file()
        response =self.client.post('/conversions/create/', data={'Name': 'test conversion', 'Type': '2', 'Upload': test_file})
        saved_items = Conversion.objects.all()
        saved_conversion_name = saved_items[0].ConvName
        self.assertEqual('ER_EAI_2nd', saved_conversion_name)
