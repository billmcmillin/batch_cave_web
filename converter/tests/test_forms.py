from django.test import TestCase
from converter.forms import ConversionForm
from converter.forms import UNNAMED_CONVERSION_ERROR, UNTYPED_CONVERSION_ERROR, NOFILE_CONVERSION_ERROR
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest import skip

class ConversionFormTest(TestCase):

    def get_test_file(self):
        with open('/data/infiles/TEST.mrc', 'rb') as testMarc:
            test_file = SimpleUploadedFile('TEST.mrc', testMarc.read())
        return test_file

    def get_file_handle(self):
        with open('/data/infiles/TEST.mrc', 'rb') as testMarc:
            return testMarc

    def test_form_name_input_has_placeholder_and_css(self):
        form = ConversionForm()
        test_file = self.get_test_file()
        self.assertIn('class="form-control input-lg"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_saves_when_complete(self):
        test_file = self.get_test_file()
        response =self.client.post('/conversions/create/', data={'Name': 'test conversion', 'Type': '2', 'Upload': test_file})
        self.assertEqual(response['location'], '/conversions/index')

    def test_form_validation_for_blank_names(self):
        test_file = self.get_test_file()
        response =self.client.post('/conversions/create/', data={'Name': '', 'Type': '2', 'Upload': test_file})
        expected_error = UNNAMED_CONVERSION_ERROR
        self.assertContains(response, expected_error)

###################################SKIP###############
    @skip
    def test_form_validation_for_blank_names(self):
        #with self.assertRaises(Exception):
        test_file = self.get_test_file()
        response =self.client.post('/conversions/create/', data={'Name': 'A name', 'Type': '', 'Upload': test_file})
        expected_error = UNTYPED_CONVERSION_ERROR
        print('ran it!')
        self.assertContains(response, expected_error)

###################################SKIP###############
    @skip
    def test_form_validation_for_blank_file(self):
        test_file = self.get_test_file()
        response =self.client.post('/conversions/create/',data={'Name':'Huhwaht', 'Type': '2', 'Upload': ''})
        expected_error = UNNAMED_CONVERSION_ERROR
        self.assertContains(response, expected_error)
