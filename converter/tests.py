from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from converter.models import Conversion

from converter.views import home_page


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class ConversionTest(TestCase):

    def test_can_save_a_POST_request(self):
        response = self.client.post('/conversions/create/', data={'conversion_name': 'A new conversion'})
        self.assertIn('A new conversion', response.content.decode())
        self.assertTemplateUsed(response, 'create.html')

class ConversionModelTest(TestCase):

    def test_saving_and_retrieving_conversions(self):
        first_conversion = Conversion()
        first_conversion.name = 'The first ever conversion'
        first_conversion.save()

        second_conversion = Conversion()
        second_conversion.name = 'Conversion the second'
        second_conversion.save()

        saved_items = Conversion.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.name, 'The first ever conversion')
        self.assertEqual(second_saved_item.name, 'Conversion the second')
