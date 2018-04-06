from django.test import TestCase
from converter.models import Conversion
from django.core.files.uploadedfile import SimpleUploadedFile

class ConversionModelTest(TestCase):

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

