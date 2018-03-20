from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

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
