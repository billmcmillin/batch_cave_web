from django.test import TestCase
from converter.models import Conversion
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest import skip
from django.core.exceptions import ValidationError

class ConversionModelTest(TestCase):

    def get_test_file(self):
        with open('/data/infiles/TEST.mrc', 'rb') as testMarc:
            test_file = SimpleUploadedFile('TEST.mrc', testMarc.read())
        return test_file

    def open_file(self, file_name):
        test_file = file_name.read()
        return test_file


###################################SKIP###############
    @skip
    def test_cannot_save_empty_conversion(self):
        conv = Conversion.objects.create()
        with self.assertRaises(ValueError):
            conv.save()
            conv.full_clean()

###################################SKIP###############
    @skip
    def test_unnamed_conversions_not_saved(self):
        test_file = self.get_test_file()
        response =self.client.post('/conversions/create/', data={'Name': '', 'Type': 1, 'Upload': test_file})
        self.assertEqual(Conversion.objects.count(), 0)

###################################SKIP###############
    @skip
    def test_blank_type_conversions_not_saved(self):
        with self.assertRaises(AttributeError):
            test_file = self.get_test_file()
            response =self.client.post('/conversions/create/', data={'Name': 'test conversion', 'Type': '', 'Upload': test_file})
            self.assertEqual(Conversion.objects.count(), 1)


###################################SKIP###############
    @skip
    def test_blank_file_conversion_not_saved(self):
        response =self.client.post('/conversions/create/', data={'Name': 'test conversion', 'Type': 1, 'Upload': '' })
        self.assertEqual(Conversion.objects.count(), 0)

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

    def test_mrk_files_are_created(self):
        test_file = self.get_test_file()
        response = self.client.post('/conversions/create/', data={'Name': 'test conversion', 'Type': '2', 'Upload': test_file})
        saved_items = Conversion.objects.all()
        mrk_in = saved_items[0].MrkIn
        mrk_out = saved_items[0].MrkOut
