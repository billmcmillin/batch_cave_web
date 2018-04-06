from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.core.files.uploadedfile import SimpleUploadedFile
from converter.models import Conversion

from converter.views import home_page


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class ConversionViewsTest(TestCase):
    def get_test_file(self):
        with open('/data/infiles/TEST.mrc', 'rb') as testMarc:
            test_file = SimpleUploadedFile('TEST.mrc', testMarc.read())
        return test_file

    def test_can_save_a_POST_request(self):
        test_file = self.get_test_file()
        self.client.post('/conversions/create/', data={'Name': 'A new conversion', 'Type': 1, 'Upload': test_file})
        self.assertEqual(Conversion.objects.count(), 1)
        new_conv = Conversion.objects.first()
        self.assertEqual('A new conversion', new_conv.Name)

    def test_redirects_after_POST(self):
        test_file = self.get_test_file()
        response =self.client.post('/conversions/create/', data={'Name': 'A new conversion', 'Type': 1, 'Upload': test_file})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/conversions/index')

    def test_uses_conv_index_template(self):
        response = self.client.get('/conversions/index')
        self.assertTemplateUsed(response, 'index.html')

    def test_only_saves_when_needed(self):
        response = self.client.get('/conversions/index')
        self.assertTemplateUsed(response, 'index.html')
        self.assertEqual(Conversion.objects.count(), 0)

    def test_displays_all_conversions(self):
        Conversion.objects.create(Name='First one')
        Conversion.objects.create(Name='Second one')

        response = self.client.get('/conversions/index')

        self.assertContains(response, 'First one')
        self.assertContains(response, 'Second one')


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

