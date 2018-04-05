from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from converter.models import Conversion
from converter.forms import ConversionForm

from converter.views import home_page


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class ConversionViewsTest(TestCase):

    def test_can_save_a_POST_request(self):
        self.client.post('/conversions/create/', data={'conversion_name': 'A new conversion'})
        self.assertEqual(Conversion.objects.count(), 1)
        new_conv = Conversion.objects.first()
        self.assertEqual('A new conversion', new_conv.name)

    def test_redirects_after_POST(self):
        response = self.client.post('/conversions/create/', data={'conversion_name': 'A new conversion'})
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
        Conversion.objects.create(name='First one')
        Conversion.objects.create(name='Second one')

        response = self.client.get('/conversions/index')

        self.assertContains(response, 'First one')
        self.assertContains(response, 'Second one')


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

class ConversionFormTest(TestCase):

    def test_form_name_input_has_placeholder_and_css(self):
        form = ConversionForm()
        self.assertIn('class="form-control input-lg"', form.as_p())
