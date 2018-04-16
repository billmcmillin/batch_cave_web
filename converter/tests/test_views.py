from django.test import TestCase
from converter.models import Conversion
from django.core.files.uploadedfile import SimpleUploadedFile
from converter.forms import ConversionForm
from converter.forms import UNNAMED_CONVERSION_ERROR, UNTYPED_CONVERSION_ERROR, NOFILE_CONVERSION_ERROR
from unittest import skip

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


    def test_create_uses_form(self):
        response = self.client.get('/conversions/create/')
        self.assertIsInstance(response.context['form'], ConversionForm)

###################################SKIP###############
    @skip
    def test_for_invalid_input_renders_create_template(self):
        response =self.client.post('/conversions/create/', data={'Name': 'ok', 'Type': 1, 'Upload': ''})

###################################SKIP###############
    @skip
    def test_validation_errors_shown_on_create_page(self):
        response =self.client.post('/conversions/create/', data={'Name': 'ok', 'Type': 1, 'Upload': ''})
        expected_error = NOFILE_CONVERSION_ERROR
        self.assertContains(response, expected_error)

###################################SKIP###############
    @skip
    def test_invalid_input_passes_form_to_template(self):
        response =self.client.post('/conversions/create/', data={'Name': 'ok', 'Type': 1, 'Upload': ''})
        self.assertIsInstance(response.context['form'], ConversionForm)
