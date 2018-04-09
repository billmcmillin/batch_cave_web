from django.test import TestCase
from converter.models import Conversion
from django.core.files.uploadedfile import SimpleUploadedFile

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

    def test_validation_errors_sent_to_template(self):
        test_file = self.get_test_file()
        response =self.client.post('/conversions/create/', data={'Name': '', 'Type': 1, 'Upload': test_file})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create.html')
        expected_error = "This field is required"
        self.assertContains(response, expected_error)

    def test_invalid_conversions_arent_saved(self):
        test_file = self.get_test_file()
        response =self.client.post('/conversions/create/', data={'Name': '', 'Type': 1, 'Upload': test_file})
        self.assertEqual(Conversion.objects.count(), 0)
