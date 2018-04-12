from django.test import TestCase
from converter.models import Conversion
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError

class ConversionModelTest(TestCase):

    def get_test_file(self):
        with open('/data/infiles/TEST.mrc', 'rb') as testMarc:
            test_file = SimpleUploadedFile('TEST.mrc', testMarc.read())
        return test_file

    def open_file(self, file_name):
        test_file = file_name.read()
        return test_file

    def test_saving_and_retrieving_conversions(self):
        first_conversion = Conversion()
        first_conversion.Name = 'The first ever conversion'
        first_conversion.save()

        second_conversion = Conversion()
        second_conversion.Name = 'Conversion the second'
        second_conversion.save()

        saved_items = Conversion.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.Name, 'The first ever conversion')
        self.assertEqual(second_saved_item.Name, 'Conversion the second')

    def test_cannot_save_empty_conversion(self):
        conv = Conversion.objects.create()
        with self.assertRaises(ValidationError):
            conv.save()
            conv.full_clean()

    def test_unnamed_conversions_not_saved(self):
        test_file = self.get_test_file()
        response =self.client.post('/conversions/create/', data={'Name': '', 'Type': 1, 'Upload': test_file})
        self.assertEqual(Conversion.objects.count(), 0)

    def test_blank_type_conversions_not_saved(self):
        test_file = self.get_test_file()
        response =self.client.post('/conversions/create/', data={'Name': 'test conversion', 'Type': '', 'Upload': test_file})
        self.assertEqual(Conversion.objects.count(), 0)


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
