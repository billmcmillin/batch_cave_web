from django.test import TestCase
from converter.forms import ConversionForm
from converter.forms import UNNAMED_CONVERSION_ERROR, UNTYPED_CONVERSION_ERROR, NOFILE_CONVERSION_ERROR
from django.core.files.uploadedfile import SimpleUploadedFile

class ConversionFormTest(TestCase):

    def get_test_file(self):
        with open('/data/infiles/TEST.mrc', 'rb') as testMarc:
            test_file = SimpleUploadedFile('TEST.mrc', testMarc.read())
        return test_file

    def test_form_name_input_has_placeholder_and_css(self):
        form = ConversionForm()
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_saves_when_complete(self):
        test_file = self.get_test_file()
        form = ConversionForm(data={'Name': 'First one', 'Type': 1, 'Upload': test_file })
        self.assertTrue(form.is_valid())

    def test_form_validation_for_blank_names(self):
        test_file = self.get_test_file()
        form = ConversionForm(data={'Name': '', 'Type': 1, 'Upload': test_file})
        self.assertFalse(form.is_valid())
        self.assertIn(
            UNNAMED_CONVERSION_ERROR,
            form.errors.as_text(),
        )

    def test_form_validation_for_blank_type(self):
        test_file = self.get_test_file()
        form = ConversionForm(data={'Name': 'Huhwhat', 'Type': '', 'Upload': test_file})
        self.assertFalse(form.is_valid())
        self.assertIn(
            UNTYPED_CONVERSION_ERROR,
            form.errors.as_text(),
        )

    def test_form_validation_for_blank_file(self):
        form = ConversionForm(data={'Name': 'Huhwhat', 'Type': 1, 'Upload': '' })
        self.assertFalse(form.is_valid())
        self.assertIn(
            NOFILE_CONVERSION_ERROR,
            form.errors.as_text(),
        )
